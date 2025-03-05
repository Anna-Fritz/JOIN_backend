from rest_framework import generics
from ..models import UserProfile
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer, RegistrationSerializer, EmailAuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            try:
                saved_account = serializer.save()
                token, _ = Token.objects.get_or_create(user=saved_account)
                return Response({
                    'token': token.key,
                    'username': saved_account.username,
                    'email': saved_account.email
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmailAuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.validated_data['user']
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'username': user.username,
                    'email': user.email,
                    'user_id': user.id
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    data = request.data

    try:
        user = User.objects.get(email=data["email"])

        if user.check_password(data["password"]):
            refresh = RefreshToken.for_user(user)

            response = Response({
                'accessToken': str(refresh.access_token),
                'username': user.username,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_200_OK)

            # When 'Remember Me' is clicked, we set a long refresh token
            max_age = 60 * 60 * 24 * 30 if data.get("remember") else 60 * 60 * 24  # 30 Tage oder 1 Tag

            # set Refresh-Token as HttpOnly-Cookie
            response.set_cookie(
                "refreshToken",
                str(refresh),
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=max_age
            )

            return response

        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def refresh_view(request):
    refresh_token = request.COOKIES.get("refreshToken")

    if not refresh_token:
        return JsonResponse({"error": "No refresh token"}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return JsonResponse({"access": access_token})
    except Exception:
        return JsonResponse({"error": "Invalid refresh token"}, status=401)


@csrf_exempt
def logout_view(request):
    response = JsonResponse({"message": "Logged out"})
    response.delete_cookie("refreshToken")
    return response