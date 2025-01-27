from celery import Celery

from src.config import settings

print(settings.redis.redis_url)

celery_app = Celery(
    "tasks", broker=settings.redis.redis_url, backend=settings.redis.redis_url
)


@celery_app.task
async def check_solution():
    pass
