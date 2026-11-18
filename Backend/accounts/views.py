from django.shortcuts import render
from datetime import timedelta

from django.utils import timezone
from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token

from .models import User
from .seralizers import loginSerializer, SetPinSerializer

MAX_FAILED_ATTEMPTS = 5
LOCK_DURATION_MINUTES = 15

class LoginView(APIView):
  authentication_classes = []
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = loginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    pin = serializer.validated_data['pin']

    user = User.objects.filter(username=username).first()

    #Message d'erreur générique pour éviter de révéler si l'utilisateur existe ou non

    invalid_response = Response({"detail": "identifaint incorrects ou compte temporairement bloqué."}, status=status.HTTP_401_UNAUTHORIZED)

    if user is None or not user.is_active:
      return invalid_response
    if user.pin_locked_until and user.pin_locked_until > timezone.now():
      return invalid_response
    if user.pin_locked_until and user.pin_locked_until <= timezone.now():
      user.pin_locked_until = None
      user.failed_pin_attempts = 0

    if not user.verify_pin(pin):
      user.pin_failed_attempts += 1
      if user.pin_failed_attempts >= MAX_FAILED_ATTEMPTS:
        user.pin_locked_until = (timezone.now() + timedelta(minutes=LOCK_DURATION_MINUTES))
      user.save(update_fields=['pin_failed_attempts', 'pin_locked_until'])
      return invalid_response

     #Connexion reussie
    user.pin_failed_attempts = 0
    user.pin_locked_until = None
    user.save(update_fields=['pin_failed_attempts', 'pin_locked_until'])

    token, created = Token.objects.get_or_create(user=user)
    return Response({
        "message": "Connexion réussie.",
        "token": token.key,
        "user": {
          "id": user.id,
          "username": user.username,
          "email": user.email,
          "first_name": user.first_name,
          "last_name": user.last_name,
        }
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    user = request.user
    Token.objects.filter(user=user).delete()
    return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK)

class ProfilView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_staff": user.is_staff,
      }, status=status.HTTP_200_OK)

class SetPinView(APIView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = SetPinSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = request.user

    with transaction.atomic():
      user.set_pin(serializer.validated_data['pin'])
      user.save(update_fields=[
        'pin_hash',
        'pin_failed_attempts',
        'pin_locked_until'
      ])

    return Response({"message": "PIN mis à jour avec succès."}, status=status.HTTP_200_OK)

