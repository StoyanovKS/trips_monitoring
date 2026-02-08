import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

app = Celery("config")


app.config_from_object("django.conf:settings", namespace="CELERY")


app.autodiscover_tasks()


app.conf.beat_schedule = {
    
    "recalculate-monthly-stats-nightly": {
        "task": "statsapp.tasks.recalculate_all_cars_current_month",
        "schedule": crontab(hour=3, minute=10),
    },
    
    "send-weekly-summary-email": {
        "task": "logbook.tasks.send_weekly_summary_for_all_users",
        "schedule": crontab(day_of_week=1, hour=9, minute=0),
    },
}