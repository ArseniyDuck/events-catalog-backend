from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import phone_validator, color_validator


class User(AbstractUser):
   phone_number = models.CharField(validators=[phone_validator], max_length=12, blank=True)
   photo = models.ImageField(upload_to='users/', null=True)
   is_profile_notification_shown = models.BooleanField(default=True)


class Category(models.Model):
   name = models.CharField(max_length=180)
   color = models.CharField(max_length=7, validators=[color_validator])

   class Meta:
      verbose_name_plural = 'categories'

   def __str__(self):
      return self.name


class Event(models.Model):
   is_active = models.BooleanField(default=True)
   name = models.CharField(max_length=360)
   description = models.TextField()
   photo = models.ImageField(upload_to='events/', blank=True)
   time = models.DateTimeField()
   people_required = models.PositiveSmallIntegerField()
   people_joined = models.PositiveSmallIntegerField()
   place = models.CharField(max_length=360)
   price = models.PositiveSmallIntegerField(blank=True, default=0)
   categories = models.ManyToManyField(Category)
   creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')

   def available_places(self):
      return self.people_required - self.people_joined

   def __str__(self):
      return self.name


class PopularCategory(models.Model):
   categories = models.ManyToManyField(Category)

   class Meta:
      verbose_name_plural = 'popular categories'

   def __str__(self):
      return ", ".join([str(i) for i in self.categories.all()])