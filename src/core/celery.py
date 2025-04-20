from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/0",  # default Redis URL
    backend="redis://localhost:6379/0",  # optional: for task result storage
)

celery_app.conf.beat_schedule = {
    "run-rag-every-5-minutes": {
        "task": "src.services.tasks.run_rag_pipeline",
        "schedule": 60.0,
        "args": (1,),
    }
}
celery_app.autodiscover_tasks(["src.services"])
celery_app.conf.timezone = "UTC"
