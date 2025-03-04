import asyncio

from docker.errors import DockerException
from sqlalchemy.ext.asyncio import AsyncSession

from celery_config import celery_app
from database import get_session
from solutions.models import (
    solutions_repo,
    SolutionModel,
    SolutionStatus,
)
from tasks.models import TaskModel, task_repo
from test_system.runners.code_runner import CodeRunner

from test_system.config import test_system_config
from test_system.runners.factory import code_runner_factory

from test_system.exceptions import (
    RunTimeException,
    TimeLimitException,
    MemoryLimitException,
    WrongAnswerException,
)
from test_system.schemas import LanguageSchema


@celery_app.task
def check_solution(solution_id: int):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_check_solution(solution_id))


async def async_check_solution(solution_id: int):
    session = await anext(get_session())
    solution_model: SolutionModel = await solutions_repo.get_one(solution_id, session)
    task_model: TaskModel = await task_repo.get_one(solution_model.task_id, session)
    language_schema: LanguageSchema = test_system_config.get_lang_scheme(
        solution_model.language
    )

    try:
        code_runner: CodeRunner = code_runner_factory.get_code_runner(
            code=solution_model.code,
            language=solution_model.language,
            task_model=task_model,
        )

        print("Code Runner created!")

        solution_model: SolutionModel = await solutions_repo.patch(
            obj_id=solution_model.id, status=SolutionStatus.COMPILING
        )

        print("Code file creating...")
        code_runner.create_file()
        print("Code File created!")

        print("Code file analyzing...")
        code_runner.analyze_code()
        print("Code File analyzed!")

        print("Code File Compilling!")
        if language_schema.compiled:
            code_runner.compile_code()
        print("Code File Compilled!")

        print("Code testing...")
        for test_number in range(1, task_model.test_count + 1):
            solution_model: SolutionModel = asyncio.run(
                solutions_repo.patch(
                    obj_id=solution_model.id,
                    status=SolutionStatus.RUNNING,
                    test_number=test_number,
                )
            )
            output = code_runner.run_test(test_number)
            print(f"Output: {output}")
        print("Code File Runned!")
    except DockerException as e:
        print(f"Ошибка при работе с Docker: {e}")
    except TimeLimitException as e:
        solution_model: SolutionModel = asyncio.run(
            solutions_repo.patch(
                obj_id=solution_model.id, status=SolutionStatus.TIME_LIMIT
            )
        )
    except MemoryLimitException as e:
        solution_model: SolutionModel = asyncio.run(
            solutions_repo.patch(
                obj_id=solution_model.id, status=SolutionStatus.MEMORY_LIMIT
            )
        )
    except RunTimeException as e:
        solution_model: SolutionModel = asyncio.run(
            solutions_repo.patch(
                obj_id=solution_model.id, status=SolutionStatus.RUNTIME_ERROR
            )
        )
    except WrongAnswerException as e:
        solution_model: SolutionModel = asyncio.run(
            solutions_repo.patch(
                obj_id=solution_model.id, status=SolutionStatus.WRONG_ANSWER
            )
        )
    else:
        solution_model: SolutionModel = asyncio.run(
            solutions_repo.patch(
                obj_id=solution_model.id, status=SolutionStatus.ACCEPTED
            )
        )
