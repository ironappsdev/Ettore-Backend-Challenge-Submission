from rest_framework import serializers
from django.contrib.auth.models import User
from core.models import UserProfile, Measurement, Recommendation, MetaPersonal


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = "__all__"


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MetaPersonal
        fields = "__all__"

class GoalUserInputSerializer(serializers.Serializer):
    message = serializers.CharField()