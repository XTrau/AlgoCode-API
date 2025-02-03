import asyncio
from asyncio import AbstractEventLoop

import docker
from celery import Celery

from config import settings
from solutions.models import solutions_repo, SolutionModel

celery_app = Celery(
    "tasks",
    broker=settings.redis.redis_url,
    backend=settings.redis.redis_url,
    broker_connection_retry_on_startup=True,
)

client = docker.from_env()


@celery_app.task
def check_solution(solution_id: int):
    loop: AbstractEventLoop = asyncio.get_event_loop()
    solution_model: SolutionModel = loop.run_until_complete(
        solutions_repo.get_one(solution_id)
    )
    try:
        container = client.containers.run(
            "python:3.9",
            "python /path/to/your/script.py",
            detach=True,
            remove=True,
        )

        logs = container.logs()
        print(logs.decode("utf-8"))

        container.wait()

    except docker.errors.DockerException as e:
        print(f"Ошибка при работе с Docker: {e}")

    # Создаем docker container для тестов
    # Помещаем в него все тесты нужного task (solution_model.task_id)
    # Тестируем в нем код, компилируем один раз, а потом запускаем RunCode на каждом тесте
    # После каждого теста записываем в solutions новые данные

    return "Hello, World!"
