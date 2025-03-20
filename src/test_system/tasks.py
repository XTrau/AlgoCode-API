from celery import Celery
from sqlalchemy.orm import Session

from config import settings
from database import get_sync_session

from tasks.models import TaskModel, task_sync_repo
from test_system.models import SolutionModel, solutions_sync_repo, SolutionStatus
from test_system.runners.code_runner import CodeRunner

from test_system.config import test_system_config
from test_system.runners.factory import code_runner_factory

from test_system.exceptions import (
    TimeLimitException,
    MemoryLimitException,
    WrongAnswerException,
)
from test_system.schemas import LanguageSchema


celery_app = Celery(
    "tasks",
    backend=settings.redis.redis_url,
    broker=settings.redis.redis_url,
    broker_connection_retry_on_startup=True,
)


def check_output(task_id: int, test_number: int, output: str):
    with open(
        test_system_config.HOST_TESTS_PATH / str(task_id) / f"output{test_number}"
    ) as file:
        expected_output = file.read().strip(" ").strip("\n")

    if output != expected_output:
        raise WrongAnswerException()


@celery_app.task
def check_solution(solution_id: int):
    session: Session = next(get_sync_session())
    solution_model: SolutionModel = solutions_sync_repo.get_one(solution_id, session)
    task_model: TaskModel = task_sync_repo.get_one(solution_model.task_id, session)
    language_schema: LanguageSchema = test_system_config.get_lang_scheme(
        solution_model.language
    )
    try:
        code_runner: CodeRunner = code_runner_factory.get_code_runner(
            code=solution_model.code,
            language=solution_model.language,
            task_model=task_model,
        )

        solution_model: SolutionModel = solutions_sync_repo.patch(
            obj_id=solution_model.id, status=SolutionStatus.COMPILING, session=session
        )

        code_runner.create_file()
        code_runner.analyze_code()
        if language_schema.compiled:
            code_runner.compile_code()

        for test_number in range(1, task_model.test_count + 1):
            solution_model: SolutionModel = solutions_sync_repo.patch(
                obj_id=solution_model.id,
                status=SolutionStatus.RUNNING,
                test_number=test_number,
                session=session,
            )
            output = code_runner.run_test(test_number)
            check_output(task_model.id, test_number, output)
    except TimeLimitException as e:
        solution_model: SolutionModel = solutions_sync_repo.patch(
            obj_id=solution_model.id,
            status=SolutionStatus.TIME_LIMIT,
            session=session,
        )

    except MemoryLimitException as e:
        solution_model: SolutionModel = solutions_sync_repo.patch(
            obj_id=solution_model.id,
            status=SolutionStatus.MEMORY_LIMIT,
            session=session,
        )
    except WrongAnswerException as e:
        solution_model: SolutionModel = solutions_sync_repo.patch(
            obj_id=solution_model.id,
            status=SolutionStatus.WRONG_ANSWER,
            session=session,
        )
    except Exception as e:
        solution_model: SolutionModel = solutions_sync_repo.patch(
            obj_id=solution_model.id,
            status=SolutionStatus.RUNTIME_ERROR,
            session=session,
        )
    else:
        solution_model: SolutionModel = solutions_sync_repo.patch(
            obj_id=solution_model.id,
            status=SolutionStatus.ACCEPTED,
            session=session,
        )
    finally:
        session.close()
