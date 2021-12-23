import re
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Event
from app.serializers import EventSerializer, RegisterSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny


class EventsView(generics.ListAPIView):
   permission_classes = [AllowAny]
   authentication_classes = [JWTAuthentication]
   model = Event
   queryset = Event.objects.all()
   serializer_class = EventSerializer


class UserView(APIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]
   def get(self, request):
      serializer = UserSerializer(request.user)
      return Response(serializer.data)


class RegisterView(generics.CreateAPIView):
   queryset = get_user_model().objects.all()
   permission_classes = (AllowAny,)
   serializer_class = RegisterSerializer