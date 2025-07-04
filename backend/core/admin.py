from django.contrib import admin
from .models import UserProfile, Measurement, Goal, Notification, Recommendation

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.get_fields()]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Measurement._meta.get_fields()]


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Goal._meta.get_fields()]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Notification._meta.get_fields()]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Recommendation._meta.get_fields()]