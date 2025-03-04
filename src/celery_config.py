from celery import Celery

from config import settings

celery_app = Celery(
    "tasks",
    broker=settings.redis.redis_url,
    backend=settings.redis.redis_url,
    broker_connection_retry_on_startup=True,
)
