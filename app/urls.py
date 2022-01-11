from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



app_name = 'app'
urlpatterns = [
   # lists
   path('events/', EventsView.as_view()),
   path('events/mine/', UserEvents.as_view()),
   path('categories/', CategoriesView.as_view()),

   # update
   path('notification/', NotificationView.as_view()),
   path('me/update/', UpdateProfileView.as_view()),

   # create
   path('event/create/', EventCreationView.as_view()),
   
   # authentication
   path('me/', UserView.as_view()),
   path('token/obtain/', TokenObtainPairView.as_view()),
   path('token/refresh/', TokenRefreshView.as_view()),
   path('register/', RegisterView.as_view()),
]