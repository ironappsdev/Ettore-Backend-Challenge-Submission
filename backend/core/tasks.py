from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Goal, Notification, Recommendation, Measurement, UserProfile
import logging
import time
from .helpers import NotificationHelper, ThresholdHelper
from .llm import OpenAIClient
from datetime import datetime, timedelta

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


@shared_task(max_retries=3)
def create_measurement(user_id, data):
    """
    Task para crear una medición.
    """
    # Simular 1 segundo de espera
    time.sleep(1)

    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        logger.error(f"User {user_id} not found")
        raise Exception(f"User {user_id} not found")
    
    try:
        measurement = Measurement(user=user, **data)
        measurement.full_clean()  # Validate model fields
        measurement.save()
        logger.info(f"Measurement created for user {user_id}: {measurement}")

        exceeds_threshold = False
        threshold_helper = ThresholdHelper(measurement.type, measurement.value)
        exceeds_threshold = threshold_helper.is_outside_threshold()

        if exceeds_threshold:
            llm_client = OpenAIClient()
            # Usaremos los ultimos 7 días con un tope de 20 mediciones para el LLM
            seven_days_ago = datetime.now() - timedelta(days=7)
            last_measurements = Measurement.objects.filter(
                user=user,
                recorded_at__gte=seven_days_ago
            ).order_by('-recorded_at')[:20]  # Con max de 20 mediciones para el LLM
            try:
                user_profile = UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                logger.error(f"UserProfile for user {user_id} not found")
                raise Exception(f"UserProfile for user {user_id} not found")
            recommendation_text = llm_client.obtener_recomendacion(user_profile, last_measurements)

            #Save the recommendation
            recommendation = Recommendation(user=user, model_output=recommendation_text)
            recommendation.save()

            notification_helper = NotificationHelper(user, 
                                                    "Alerta de salud", 
                                                    f"La medición {measurement.type} está fuera de rango.\n\nRecomendación: {recommendation_text}")
            notification_helper.send_notification()

        return measurement.id
    except Exception as e:
        logger.error(f"Unexpected error creating measurement for user {user_id}: {e}")
        return None


@shared_task(max_retries=3)
def create_recommendation(user_id):
    """
    Task para crear una recomendación.
    """
    # Simular 1 segundo de espera
    time.sleep(1)

    if User.objects.filter(id=user_id).exists():
        user = User.objects.get(id=user_id)
    else:
        logger.error(f"User {user_id} not found")
        raise Exception(f"User {user_id} not found")
    
    try:
        llm_client = OpenAIClient()
        # Usaremos los ultimos 7 días con un tope de 20 mediciones para el LLM
        seven_days_ago = datetime.now() - timedelta(days=7)
        last_measurements = Measurement.objects.filter(
            user=user,
            recorded_at__gte=seven_days_ago
        ).order_by('-recorded_at')[:20]  # Con max de 20 mediciones para el LLM
        try:
            user_profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            logger.error(f"UserProfile for user {user_id} not found")
            raise Exception(f"UserProfile for user {user_id} not found")
        recommendation_text = llm_client.obtener_recomendacion(user_profile, last_measurements)
        
        recommendation = Recommendation(user=user, model_output=recommendation_text)
        recommendation.save()
        return recommendation.id
    
    except Exception as e:
        logger.error(f"Unexpected error creating recommendation for user {user_id}: {e}")
        return None