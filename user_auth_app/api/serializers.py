from rest_framework import serializers
from ..models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserProfile model, handling serialization and deserialization
    of user-related profile information such as bio and location.
    """
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'location']


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration, including password confirmation and validation.

    Validates that the password and confirmed_password match and ensures that the email
    is not already in use. This serializer is used to create a new user with password hashing.
    """
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
        """
        Validates the registration data, ensuring that the password and confirmed_password match
        and that the provided email is not already in use.
        """
        pw = data['password']
        confirmed_pw = data['confirmed_password']

        if pw != confirmed_pw:
            raise serializers.ValidationError({'error': 'Passwords do not match'})

        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'error': 'Invalid email or password'})

        return data

    def create(self, validated_data):
        """
        Creates a new user instance, excluding the 'confirmed_password' field.
        This method uses the create_user method to hash the password and save the user.
        """
        validated_data.pop('confirmed_password')
        return User.objects.create_user(**validated_data)


class EmailAuthTokenSerializer(serializers.Serializer):
    """
    Serializer for email authentication, used to validate user credentials and return a user instance.

    It verifies that the provided email and password match an existing user and returns the user
    instance upon successful authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        """
        Validates the email and password, ensuring that both are provided and that they correspond
        to a valid user. If authentication is successful, the user instance is included in the
        validated attributes.
        """
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
