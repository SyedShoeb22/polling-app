# LXP/polls/apps.py
from django.apps import AppConfig

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'

    def ready(self):
        from .fastapi_runner import run_fastapi
        run_fastapi()
