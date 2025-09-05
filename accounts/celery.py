from celery import Celery

# Use the project name as the app name
app = Celery('adlm_skillhub_backend')

# Load configuration from settings.py
app.config_from_object('core.settings', namespace='CELERY')

# Auto-discover tasks in the accounts app
app.autodiscover_tasks(['accounts'], force=True)

# Optional: Log setup for debugging
import logging
logger = logging.getLogger(__name__)
logger.info("Celery app initialized for adlm_skillhub_backend")