# Call with `python manage.py init_dummy_data` to create a demo user and sample measurements.

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile, Measurement, MeasurementType, Gender, ActivityLevel
from django.utils import timezone

DEFAULT_USERNAME = "demo_user"


class Command(BaseCommand):
    help = "Create a dummy user with profile and sample measurements"

    def handle(self, *args, **kwargs):
        if User.objects.filter(username=DEFAULT_USERNAME).exists():
            self.stdout.write(
                self.style.WARNING("Demo user already exists. Skipping creation.")
            )
            return

        user = User.objects.create_user(username=DEFAULT_USERNAME, password="demo1234")
        profile = UserProfile.objects.create(
            user=user,
            gender=Gender.MALE,
            age=42,
            weight_kg=97.5,
            height_cm=179,
            chronic_conditions="hypertension, diabetes",
            activity_level=ActivityLevel.MODERATE,
        )

        Measurement.objects.create(
            user=user,
            type=MeasurementType.BP_SYS,
            value=145,
            unit="mmHg",
            recorded_at=timezone.now(),
        )

        Measurement.objects.create(
            user=user,
            type=MeasurementType.BP_DIA,
            value=90,
            unit="mmHg",
            recorded_at=timezone.now(),
        )

        Measurement.objects.create(
            user=user,
            type=MeasurementType.GLUCOSE,
            value=120,
            unit="mg/dL",
            recorded_at=timezone.now(),
        )

        self.stdout.write(
            self.style.SUCCESS("Dummy user, profile, and measurements created.")
        )
