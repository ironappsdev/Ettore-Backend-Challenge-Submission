from django.contrib import admin
from .models import UserProfile, Measurement, MetaPersonal, NotificacionSimulada, Recommendation

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UserProfile._meta.get_fields()]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Measurement._meta.get_fields()]


@admin.register(MetaPersonal)
class MetaPersonalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetaPersonal._meta.get_fields()]


@admin.register(NotificacionSimulada)
class NotificacionSimuladaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in NotificacionSimulada._meta.get_fields()]


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Recommendation._meta.get_fields()]