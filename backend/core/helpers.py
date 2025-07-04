from core.models import Notification, MeasurementType
import logging

logger = logging.getLogger(__name__)


class NotificationHelper:
    def __init__(self, user_id, title, message):
        self.user_id = user_id
        self.title = title
        self.message = message

    def send_notification(self):
        Notification.objects.create(
            user=self.user_id,
            title=self.title,
            message=self.message
        )

        #TODO: Implementar la notificación
        pass


class ThresholdHelper:
    def __init__(self, measurement_type: MeasurementType, measurement_value: float):
        self.measurement_type = measurement_type
        self.measurement_value = measurement_value
        logger.info(f"ThresholdHelper initialized for {self.measurement_type} with value {self.measurement_value}")
        logger.info(f"Upper threshold: {self.get_upper_threshold()}")
        logger.info(f"Lower threshold: {self.get_lower_threshold()}")
        logger.info(f"Is above threshold: {self.is_above_threshold()}")
        logger.info(f"Is below threshold: {self.is_below_threshold()}")
        logger.info(f"Is within threshold: {self.is_within_threshold()}")
        logger.info(f"Is outside threshold: {self.is_outside_threshold()}")

    def get_upper_threshold(self) -> float:
        if self.measurement_type == MeasurementType.BP_SYS:
            # systolic blood pressure threshold logic
            return 120
        elif self.measurement_type == MeasurementType.GLUCOSE:
            # glucose threshold logic
            return 100
        elif self.measurement_type == MeasurementType.DUMMY:
            return 100
        else:
            return None

    def get_lower_threshold(self) -> float:
        if self.measurement_type == MeasurementType.BP_SYS:
            # systolic blood pressure threshold logic
            return 80
        elif self.measurement_type == MeasurementType.GLUCOSE:
            # glucose threshold logic
            return 70
        elif self.measurement_type == MeasurementType.DUMMY:
            return 0
        else:
            return None

    def is_above_threshold(self) -> bool:
        upper_threshold = self.get_upper_threshold()
        return self.measurement_value > upper_threshold
    
    def is_below_threshold(self) -> bool:
        lower_threshold = self.get_lower_threshold()
        return self.measurement_value < lower_threshold
    
    def is_within_threshold(self) -> bool:
        upper_threshold = self.get_upper_threshold()
        lower_threshold = self.get_lower_threshold()
        return self.measurement_value > lower_threshold and self.measurement_value < upper_threshold
    
    def is_outside_threshold(self) -> bool:
        return not self.is_within_threshold()