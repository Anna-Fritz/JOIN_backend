from rest_framework import serializers
from ..models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirmed_password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, data):
        pw = data['password']
        confirmed_pw = data['confirmed_password']

        if pw != confirmed_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Invalid email or password'})

        return data

    def create(self, validated_data):
        validated_data.pop('confirmed_password')
        return User.objects.create_user(**validated_data)


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({'error': 'Invalid email or password'})

            user = authenticate(username=user.username, password=password)

            if not user:
                raise serializers.ValidationError({'error': 'Invalid email or password'})
        else:
            raise serializers.ValidationError({'error': 'Must include "email" and "password"'})

        attrs['user'] = user
        return attrs
