from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, ProfileUpdateSerializer
from .permissions import (
    IsOwnerOrReadOnly, IsAdminUserOrReadOnly, IsSameUserAllowEditionOrReadOnly
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.decorators import api_view
from rest_framework.generics import (
    RetrieveUpdateAPIView,
    ListAPIView
)
from datetime import datetime, timezone
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView

from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all().order_by('first_name')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSameUserAllowEditionOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class ProfileUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        # email send_email


# @api_view(['GET'])
# def get_aniversariantes(request):
#     now = datetime.now(timezone.utc)
#     month = now.month
#     day = now.day
#     print(f'day= {day}')
#     print(f'month= {month}')
#     aniversariantes = Profile.objects.filter(
#         data_nascimento__day=day).filter(data_nascimento__month=month)

#     print(f'aniversariantes = {aniversariantes}')

#     return Response({
#         "aniversariantes": ProfileSerializer(aniversariantes, many=True).data})
