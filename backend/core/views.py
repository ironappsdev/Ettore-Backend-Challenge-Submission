from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.models import UserProfile, Measurement
from django.contrib.auth.models import User
from core.serializers import (
    UserSerializer,
    UserProfileSerializer,
    MeasurementSerializer,
)
from .tasks import create_measurement


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