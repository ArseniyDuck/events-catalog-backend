from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth import get_user_model, login
from django.contrib.auth.password_validation import validate_password
from .models import Category, Event, PopularCategory


class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = ('id', 'name', 'color', )

   
class PopularCategoriesSeializer(CategorySerializer):
   is_popular = serializers.SerializerMethodField()

   def get_is_popular(self, obj):
      popular_categories = PopularCategory.objects.first().categories
      return popular_categories.filter(pk=obj.pk).exists()

   class Meta(CategorySerializer.Meta):
      fields  = CategorySerializer.Meta.fields + ('is_popular', )


class CreatorSerializer(serializers.ModelSerializer):
   fullname = serializers.CharField(source='get_full_name')

   class Meta:
      model = get_user_model()
      fields = ('id', 'fullname', 'phone_number', 'photo', )


class EventSerializer(serializers.ModelSerializer):
   categories = CategorySerializer(many=True)
   creator = CreatorSerializer()
   
   class Meta:
      model = Event
      exclude = ('is_active', )


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = get_user_model()
      fields = ('id', 'username', )


class RegisterSerializer(serializers.ModelSerializer):
   password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
   password2 = serializers.CharField(write_only=True, required=True)

   class Meta:
      model = get_user_model()
      fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number')

   def validate(self, attrs):
      if attrs['password1'] != attrs['password2']:
         raise serializers.ValidationError({'password1': 'Password fields didn\'t match.'})
      return attrs

   def create(self, validated_data):
      User = get_user_model()
      user = User.objects.create_user(validated_data['username'])
      user.set_password(validated_data['password1'])
      user.first_name = validated_data['first_name']
      user.last_name = validated_data['last_name']
      user.phone_number = validated_data['phone_number']
      user.save()
      login(self.context['request'], user)
      return user