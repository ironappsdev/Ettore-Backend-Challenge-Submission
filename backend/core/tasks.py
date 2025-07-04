from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Goal, Notification, Recommendation, Measurement
import logging
import time

logger = logging.getLogger(__name__)
User = get_user_model()


@shared_task
def test_task(user_id, **kwargs):
    """
    Task de prueba para verificar que el celery está funcionando.
    """
    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        logger.error(f"User {user_id} not found")
    
    for i in range(10):
        logger.info(f"Task en el paso {i}. Usuario: {user.username}")
        time.sleep(1)
    
    logger.info(f"Task finalizada. Usuario: {user.username}")
    return True


