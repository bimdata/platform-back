from platform_back.settings.environ import env

CELERY_IMPORTS = ("platform_back.tasks.notifications",)
CELERY_WORKER_CONCURRENCY = env.int("CELERY_WORKER_CONCURRENCY", default=2)


RABBITMQ_HOST = env("RABBITMQ_HOST")
RABBITMQ_USER = env("RABBITMQ_USER")
RABBITMQ_PASSWORD = env("RABBITMQ_PASSWORD")
RABBITMQ_PORT = env("RABBITMQ_PORT")

CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/"
)

CELERY_TASK_ROUTES = {
    "platform_back.tasks.*": {"queue": "celery_platform_back"},
}
