from django.db import models
from django.contrib.auth import get_user_model

USER = get_user_model()

# Create your models here.


class Gender(models.TextChoices):
    MALE = "MAL", "Male"
    FEMALE = "FEM", "Female"
    TRANS_MALE = "TMA", "Trans Male"
    TRANS_FEMALE = "TFE", "Trans female"
    OTHER = "OTR", "Other"
    UNKNOWN = "UNK", "Unknown"


class ActivityLevel(models.TextChoices):
    SEDENTARY = "sedentary", "Sedentary"
    LIGHT = "light", "Light"
    MODERATE = "moderate", "Moderate"
    INTENSE = "intense", "Intense"
    ATHLETE = "athlete", "Athlete"
    UNKNOWN = "unknown", "Unknown"


class UserProfile(models.Model):

    user = models.OneToOneField(USER, on_delete=models.CASCADE)
    gender = models.CharField(
        max_length=3, choices=Gender.choices, default=Gender.UNKNOWN
    )
    age = models.PositiveIntegerField(blank=True, null=True)
    weight_kg = models.FloatField(blank=True, null=True)
    height_cm = models.FloatField(blank=True, null=True)
    chronic_conditions = models.TextField(
        blank=True, help_text="Comma-separated list (e.g., hypertension, diabetes)"
    )
    activity_level = models.CharField(
        max_length=20, choices=ActivityLevel.choices, default=ActivityLevel.UNKNOWN
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


class MeasurementType(models.TextChoices):
    BP_SYS = "bp_sys", "Blood Pressure - Systolic"
    BP_DIA = "bp_dia", "Blood Pressure - Diastolic"
    GLUCOSE = "glucose", "Blood Glucose"
    HEART_RATE = "heart_rate", "Heart Rate"
    SATURATION = "saturation", "Oxygen Saturation"
    STEPS = "steps", "Steps"
    WEIGHT = "weight", "Weight"
    HEIGHT = "height", "Height"
    TEMPERATURE = "temperature", "Body Temperature"
    BODY_FAT = "body_fat", "Body Fat Percentage"
    CUSTOM = "custom", "Custom"
    DUMMY = "dummy", "Dummy"  # For testing purposes


class Measurement(models.Model):

    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20, choices=MeasurementType.choices, default=MeasurementType.DUMMY
    )
    type_other = models.CharField(max_length=20, blank=True, null=True)
    value = models.FloatField()
    unit = models.CharField(max_length=20)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.type if self.type != MeasurementType.CUSTOM else self.type_other}: {self.value} {self.unit} at {self.recorded_at}"


class Goal(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    user_input = models.TextField(blank=True, null=True)
    model_output = models.TextField(blank=True, null=True)
    model_name = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)
    target_value = models.FloatField(blank=True, null=True)
    target_unit = models.CharField(max_length=20, blank=True, null=True)
    target_type = models.CharField(max_length=20, blank=True, null=True)
    target_description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.model_output[:100]}"
    

class Notification(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Recommendation(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE)
    model_output = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.model_output[:100]}"