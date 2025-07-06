from core.models import NotificacionSimulada, MeasurementType
import logging

logger = logging.getLogger(__name__)


class NotificationHelper:
    def __init__(self, user_id, title, message):
        self.user_id = user_id
        self.title = title
        self.message = message

    def send_notification(self):
        NotificacionSimulada.objects.create(
            user=self.user_id,
            title=self.title,
            message=self.message
        )

        #TODO: Implementar la notificación
        pass


# WARNING: NO TENGO CONOCIMIENTOS MEDICOS, ESTO ES UNA PRUEBA GENERADA POR UN LLM
class ThresholdHelper:
    EXPECTED_UNITS = {
        MeasurementType.BP_SYS: ["mmhg", "mmHg"],
        MeasurementType.BP_DIA: ["mmhg", "mmHg"],
        MeasurementType.GLUCOSE: ["mg/dl", "mg/dL", "mmol/l", "mmol/L"],
        MeasurementType.HEART_RATE: ["bpm", "beats/min"],
        MeasurementType.SATURATION: ["%", "percent"],
        MeasurementType.STEPS: ["steps", "count"],
        MeasurementType.WEIGHT: ["kg", "lbs", "lb"],
        MeasurementType.HEIGHT: ["cm", "in", "inch", "ft"],
        MeasurementType.TEMPERATURE: ["°c", "°f", "celsius", "fahrenheit", "c", "f"],
        MeasurementType.BODY_FAT: ["%", "percent"],
        MeasurementType.DUMMY: ["unit"],
    }

    def __init__(self, measurement_type: MeasurementType, measurement_value: float, measurement_unit: str, user_profile=None):
        self.measurement_type = measurement_type
        self.measurement_value = measurement_value
        self.measurement_unit = measurement_unit.lower().strip()
        self.user_profile = user_profile
        self.is_valid_unit = self._validate_unit()
        
        if not self.is_valid_unit:
            logger.warning(f"Invalid unit '{measurement_unit}' for {self.measurement_type}. Expected: {self.EXPECTED_UNITS.get(self.measurement_type, [])}")
            return
            
        # Convert to standard units if needed
        self.normalized_value = self._normalize_value()
        
        logger.info(f"ThresholdHelper initialized for {self.measurement_type} with value {self.normalized_value}")
        logger.info(f"Upper threshold: {self.get_upper_threshold()}")
        logger.info(f"Lower threshold: {self.get_lower_threshold()}")
        logger.info(f"Is above threshold: {self.is_above_threshold()}")
        logger.info(f"Is below threshold: {self.is_below_threshold()}")
        logger.info(f"Is within threshold: {self.is_within_threshold()}")
        logger.info(f"Is outside threshold: {self.is_outside_threshold()}")
    
    def _validate_unit(self) -> bool:
        """Check if the measurement unit is valid for the measurement type"""
        expected_units = self.EXPECTED_UNITS.get(self.measurement_type, [])
        return any(self.measurement_unit == unit.lower() for unit in expected_units)
    
    def _normalize_value(self) -> float:
        """Convert measurement to standard units for threshold comparison"""
        if not self.is_valid_unit:
            return self.measurement_value
            
        # Convert glucose from mmol/L to mg/dL if needed
        if self.measurement_type == MeasurementType.GLUCOSE:
            if self.measurement_unit in ["mmol/l", "mmol/L"]:
                return self.measurement_value * 18.0  # Convert mmol/L to mg/dL
                
        # Convert weight from lbs to kg if needed
        elif self.measurement_type == MeasurementType.WEIGHT:
            if self.measurement_unit in ["lbs", "lb"]:
                return self.measurement_value * 0.453592  # Convert lbs to kg
                
        # Convert height from inches/feet to cm if needed
        elif self.measurement_type == MeasurementType.HEIGHT:
            if self.measurement_unit in ["in", "inch"]:
                return self.measurement_value * 2.54  # Convert inches to cm
            elif self.measurement_unit == "ft":
                return self.measurement_value * 30.48  # Convert feet to cm
                
        # Convert temperature from Fahrenheit to Celsius if needed
        elif self.measurement_type == MeasurementType.TEMPERATURE:
            if self.measurement_unit in ["°f", "fahrenheit", "f"]:
                return (self.measurement_value - 32) * 5/9  # Convert F to C
                
        # No conversion needed, return original value
        return self.measurement_value
    
    def _get_age(self) -> int:
        return self.user_profile.age if self.user_profile and self.user_profile.age else 40
    
    def _get_gender(self) -> str:
        return self.user_profile.gender if self.user_profile else "UNK"
    
    def _get_activity_level(self) -> str:
        return self.user_profile.activity_level if self.user_profile else "unknown"
    
    def _has_condition(self, condition: str) -> bool:
        if not self.user_profile or not self.user_profile.chronic_conditions:
            return False
        conditions = [c.strip().lower() for c in self.user_profile.chronic_conditions.split(',')]
        return condition.lower() in conditions
    
    def _get_bmi(self) -> float:
        if (self.user_profile and self.user_profile.weight_kg and 
            self.user_profile.height_cm and self.user_profile.height_cm > 0):
            height_m = self.user_profile.height_cm / 100
            return self.user_profile.weight_kg / (height_m ** 2)
        return 22.5  # Normal BMI default
    
    def get_upper_threshold(self) -> float:
        age = self._get_age()
        gender = self._get_gender()
        activity_level = self._get_activity_level()
        
        if self.measurement_type == MeasurementType.BP_SYS:
            # Base threshold
            upper = 130
            # Age adjustments - more lenient for elderly
            if age >= 65:
                upper = 140
            elif age < 18:
                upper = 120
            # Diabetes = stricter control
            if self._has_condition("diabetes"):
                upper = 130
            # Hypertension = already diagnosed, different targets
            if self._has_condition("hypertension"):
                upper = 140
            return upper
            
        elif self.measurement_type == MeasurementType.BP_DIA:
            upper = 80
            if age >= 65:
                upper = 90
            elif age < 18:
                upper = 75
            if self._has_condition("diabetes"):
                upper = 80
            if self._has_condition("hypertension"):
                upper = 90
            return upper
            
        elif self.measurement_type == MeasurementType.GLUCOSE:
            upper = 100  # Fasting glucose
            if self._has_condition("diabetes"):
                upper = 130  # Less strict for known diabetics
            elif self._has_condition("prediabetes"):
                upper = 100  # Maintain strict control
            return upper
            
        elif self.measurement_type == MeasurementType.HEART_RATE:
            upper = 100
            # Age adjustments
            if age < 18:
                upper = 120
            elif age >= 65:
                upper = 90
            # Athletes have different ranges
            if activity_level == "athlete":
                upper = 70
            elif activity_level == "intense":
                upper = 80
            return upper
            
        elif self.measurement_type == MeasurementType.SATURATION:
            upper = 100
            # COPD patients may have different targets
            if self._has_condition("copd"):
                upper = 100  # Still aim for normal
            return upper
            
        elif self.measurement_type == MeasurementType.STEPS:
            base_steps = 10000
            # Age adjustments
            if age >= 65:
                base_steps = 7500
            elif age < 18:
                base_steps = 12000
            # Activity level adjustments
            if activity_level == "athlete":
                base_steps = 15000
            elif activity_level == "intense":
                base_steps = 12000
            elif activity_level == "sedentary":
                base_steps = 6000
            return base_steps
            
        elif self.measurement_type == MeasurementType.WEIGHT:
            # BMI-based calculation
            if self.user_profile and self.user_profile.height_cm:
                height_m = self.user_profile.height_cm / 100
                # BMI 25 as upper threshold (overweight)
                upper_weight = 25.0 * (height_m ** 2)
                # Athletes can have higher BMI due to muscle
                if activity_level == "athlete":
                    upper_weight = 27.0 * (height_m ** 2)
                return upper_weight
            return 85  # Default if no height
            
        elif self.measurement_type == MeasurementType.HEIGHT:
            # Height doesn't change much in adults
            if gender in ["MAL", "TMA"]:  # Male or Trans Male
                return 200
            else:
                return 185
                
        elif self.measurement_type == MeasurementType.TEMPERATURE:
            upper = 37.5
            # Children may have slightly higher normal temps
            if age < 12:
                upper = 37.8
            return upper
            
        elif self.measurement_type == MeasurementType.BODY_FAT:
            # Gender and age specific
            if gender in ["MAL", "TMA"]:  # Male or Trans Male
                if age < 30:
                    upper = 15
                elif age < 50:
                    upper = 20
                else:
                    upper = 25
            else:  # Female, Trans Female, Other, or Unknown
                if age < 30:
                    upper = 24
                elif age < 50:
                    upper = 28
                else:
                    upper = 32
            # Athletes have lower body fat
            if activity_level == "athlete":
                upper -= 5
            return upper
            
        elif self.measurement_type == MeasurementType.DUMMY:
            return 100
            
        else:
            return 100
    
    def get_lower_threshold(self) -> float:
        age = self._get_age()
        gender = self._get_gender()
        activity_level = self._get_activity_level()
        
        if self.measurement_type == MeasurementType.BP_SYS:
            lower = 90
            # Athletes may have lower BP
            if activity_level == "athlete":
                lower = 80
            # Elderly may tolerate lower BP differently
            if age >= 65:
                lower = 90
            return lower
            
        elif self.measurement_type == MeasurementType.BP_DIA:
            lower = 60
            if activity_level == "athlete":
                lower = 50
            return lower
            
        elif self.measurement_type == MeasurementType.GLUCOSE:
            lower = 70
            # Diabetics may have different hypoglycemia thresholds
            if self._has_condition("diabetes"):
                lower = 80  # Slightly higher to avoid dangerous lows
            return lower
            
        elif self.measurement_type == MeasurementType.HEART_RATE:
            lower = 60
            # Athletes have much lower resting HR
            if activity_level == "athlete":
                lower = 40
            elif activity_level == "intense":
                lower = 50
            # Age adjustments
            if age < 18:
                lower = 70
            elif age >= 65:
                lower = 55
            return lower
            
        elif self.measurement_type == MeasurementType.SATURATION:
            lower = 95
            # COPD patients may have chronically lower O2
            if self._has_condition("copd"):
                lower = 88
            # Elderly may have slightly lower baseline
            if age >= 65:
                lower = 92
            return lower
            
        elif self.measurement_type == MeasurementType.STEPS:
            base_steps = 3000
            # Age adjustments
            if age >= 65:
                base_steps = 2000
            elif age < 18:
                base_steps = 4000
            return base_steps
            
        elif self.measurement_type == MeasurementType.WEIGHT:
            # BMI-based calculation
            if self.user_profile and self.user_profile.height_cm:
                height_m = self.user_profile.height_cm / 100
                # BMI 18.5 as lower threshold (underweight)
                lower_weight = 18.5 * (height_m ** 2)
                return lower_weight
            return 45  # Default if no height
            
        elif self.measurement_type == MeasurementType.HEIGHT:
            # Adult height minimums
            if gender in ["MAL", "TMA"]:  # Male or Trans Male
                return 150
            else:
                return 140
                
        elif self.measurement_type == MeasurementType.TEMPERATURE:
            lower = 36.0
            # Elderly may have lower baseline temps
            if age >= 65:
                lower = 35.8
            return lower
            
        elif self.measurement_type == MeasurementType.BODY_FAT:
            # Gender specific minimums
            if gender in ["MAL", "TMA"]:  # Male or Trans Male
                lower = 5
                if activity_level == "athlete":
                    lower = 3
            else:  # Female, Trans Female, Other, or Unknown
                lower = 12
                if activity_level == "athlete":
                    lower = 8
            return lower
            
        elif self.measurement_type == MeasurementType.DUMMY:
            return 0
            
        else:
            return 0
    
    def is_above_threshold(self) -> bool:
        if not self.is_valid_unit:
            return False
        upper_threshold = self.get_upper_threshold()
        return self.normalized_value > upper_threshold
    
    def is_below_threshold(self) -> bool:
        if not self.is_valid_unit:
            return False
        lower_threshold = self.get_lower_threshold()
        return self.normalized_value < lower_threshold
    
    def is_within_threshold(self) -> bool:
        if not self.is_valid_unit:
            return False
        upper_threshold = self.get_upper_threshold()
        lower_threshold = self.get_lower_threshold()
        return lower_threshold <= self.normalized_value <= upper_threshold
    
    def is_outside_threshold(self) -> bool:
        if not self.is_valid_unit:
            return True  # Invalid units are considered "outside" normal range
        return not self.is_within_threshold()