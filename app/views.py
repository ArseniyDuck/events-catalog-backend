import re
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models.expressions import ExpressionWrapper
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from rest_framework import generics, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Category, Event
from app.serializers import EventSerializer, PopularCategoriesSeializer, RegisterSerializer, UpdateProfileSerializer, UserEventSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class EventsView(generics.ListAPIView):
   permission_classes = [AllowAny]
   authentication_classes = [JWTAuthentication]
   serializer_class = EventSerializer
   filter_backends = [filters.SearchFilter, filters.OrderingFilter]
   search_fields = ['name']
   ordering_fields = ['id', 'price', 'time']

   def get_queryset(self):
      queryset = Event.objects.filter(is_active=True)

      price = self.request.query_params.get('price')
      if price is not None:
         queryset = queryset.filter(price__lte=int(price))

      time = self.request.query_params.get('time')
      if time is not None:
         pass

      people_required = self.request.query_params.get('people_required')
      if people_required is not None:
         queryset = queryset.filter(people_required__lte=int(people_required))

      available_places = self.request.query_params.get('available_places')
      if available_places is not None:
         q_ids = [o.id for o in queryset if o.available_places() >= int(available_places)]
         queryset = queryset.filter(id__in=q_ids)

      only_free = self.request.query_params.get('only_free')
      if only_free is not None:
         queryset = queryset.filter(Q(price=0))

      category_ids = self.request.query_params.get('categories')
      if category_ids is not None:
         category_ids = [int(i) for i in category_ids.split(' ')]
         queryset = queryset.filter(categories__id__in=category_ids).distinct()

      return queryset


class UserEvents(generics.ListAPIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]
   serializer_class = UserEventSerializer
   filter_backends = [filters.SearchFilter]
   search_fields = ['name']
   def get_queryset(self):
      return Event.objects.filter(creator=self.request.user)


class EventCreationView(generics.CreateAPIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]
   serializer_class = EventSerializer


class CategoriesView(generics.ListAPIView):
   permission_classes = [AllowAny]
   authentication_classes = [JWTAuthentication]
   queryset = Category.objects.all().order_by('name')
   serializer_class = PopularCategoriesSeializer


class UserView(APIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]
   def get(self, request):
      serializer = UserSerializer(request.user)
      return Response(serializer.data)

   
class NotificationView(APIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]
   def delete(self, request):
      request.user.is_profile_notification_shown = False
      request.user.save()
      return HttpResponse(status=204)


class RegisterView(generics.CreateAPIView):
   queryset = get_user_model().objects.all()
   permission_classes = (AllowAny,)
   serializer_class = RegisterSerializer


class UpdateProfileView(APIView):
   permission_classes = [IsAuthenticated]
   authentication_classes = [JWTAuthentication]
   def patch(self, request):
      validator = UpdateProfileSerializer(data=request.data)

      if validator.is_valid():
         post_data = validator.data
         request.user.first_name = post_data.get('first_name')
         request.user.last_name = post_data.get('last_name')
         request.user.phone_number = post_data.get('phone_number')
         request.user.save()
         serializer = UserSerializer(request.user)
         return Response(serializer.data, status=200)
      else:
         return Response(validator.errors, status=400)