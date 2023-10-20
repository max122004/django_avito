from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializer import UserCreateSerializer, UserDeleteSerializer, UserDetailSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse(status=status.HTTP_200_OK)


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer

