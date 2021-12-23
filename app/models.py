from django import forms
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message='Phone number must be entered in the format: \'+999999999\'. Up to 15 digits allowed.')
   phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
   photo = models.ImageField(upload_to='users/', blank=True)


class Category(models.Model):
   name = models.CharField(max_length=180)
   color_regex = RegexValidator(regex=r'^#(?:[0-9a-fA-F]{3}){1,2}$', message='Color must be in hex')
   color = models.CharField(max_length=7, validators=[color_regex])

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
   price = models.PositiveSmallIntegerField(blank=True, null=True)
   categories = models.ManyToManyField(Category)
   creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')

   def __str__(self):
      return self.name


class PopularCategory(models.Model):
   categories = models.ManyToManyField(Category)

   class Meta:
      verbose_name_plural = 'popular categories'

   def __str__(self):
      return ", ".join([str(i) for i in self.categories.all()])