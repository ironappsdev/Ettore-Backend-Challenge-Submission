from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import UserProfile, Measurement, Recommendation, MetaPersonal
from django.contrib.auth.models import User
from core.serializers import (
    UserSerializer,
    UserProfileSerializer,
    MeasurementSerializer,
    RecommendationSerializer,
    GoalSerializer,
    GoalUserInputSerializer,
)
from .tasks import create_measurement, create_recommendation, create_goal


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data.copy()

        if 'user' in validated_data:
            del validated_data['user']

        create_measurement.delay(request.user.id, validated_data)
        return Response({'detail': 'Measurement creation scheduled.'}, status=status.HTTP_202_ACCEPTED)


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        queryset = self.get_queryset()
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id') or request.user.id
        if user_id is None:
            return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        create_recommendation.delay(user_id)
        return Response({'detail': 'Recommendation creation scheduled.'}, status=status.HTTP_202_ACCEPTED)


class GoalViewSet(viewsets.ModelViewSet):
    queryset = MetaPersonal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return GoalUserInputSerializer
        return GoalSerializer

    def create(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        message = input_serializer.validated_data['message']

        create_goal.delay(request.user.id, message)
        return Response({'detail': 'Goal creation scheduled.'}, status=status.HTTP_202_ACCEPTED)