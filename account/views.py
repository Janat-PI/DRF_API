from django.shortcuts import render
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import RegisterSerializer, ActivationSerializer, LoginSerialiser

'''
1) Регистрация 
2) Активация
3) Логин 
4) восстановление пароля
5) Смена пароля
6) Профиль пользователя
'''


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('your account successfully registration', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.activate()
        return Response('your account successfully activate!', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerialiser