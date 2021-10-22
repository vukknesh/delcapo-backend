from rest_framework import serializers
from django.contrib.auth.models import User


from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    CharField,
    BooleanField,
    ImageField,
    ValidationError,
    HyperlinkedModelSerializer,
    ReadOnlyField,
    IntegerField,
)
from django.shortcuts import get_object_or_404
from .models import Profile
from datetime import datetime, timezone, date


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_id = ReadOnlyField(source="profile.id")
    profile = ReadOnlyField(source="profile")

    class Meta:
        model = User
        depth = 1
        fields = ('id',  'username', 'first_name', 'profile_id', 'profile',
                  'email',)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    first_name = CharField(source='user.first_name')
    email = CharField(source='user.email')
    ativo = BooleanField(source='user.is_active')

    class Meta:
        model = Profile
        depth = 1
        fields = ('id', 'slug', 'ativo', 'first_name', 'email', 'endereco',  'fone',
                  'created_at', 'updated')

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # First, update the User
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # Then, update UserProfile

        for attr, value in validated_data.items():
            print(validated_data)
            setattr(instance, attr, value)
            instance.save()
        return instance


class ProfileUpdateSerializer(ModelSerializer):
    user = ReadOnlyField(source='user.id')

    class Meta:
        model = Profile
        fields = ('id', 'slug', 'first_name',
                  'user', 'created_at', 'updated')
