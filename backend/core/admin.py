from django.contrib import admin
from .models import UserProfile, Measurement

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.get_fields()]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Measurement._meta.get_fields()]
