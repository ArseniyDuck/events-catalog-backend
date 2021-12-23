from rest_framework import serializers
from django.contrib.auth import get_user_model, login
from django.contrib.auth.password_validation import validate_password
from .models import Category, Event


class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model = Category
      fields = '__all__'


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
      fields = '__all__'


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