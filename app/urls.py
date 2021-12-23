from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



app_name = 'app'
urlpatterns = [
   path('events/', EventsView.as_view()),
   
   # authentication
   path('me/', UserView.as_view()),
   path('token/obtain/', TokenObtainPairView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view()),
   path('register/', RegisterView.as_view()),
]