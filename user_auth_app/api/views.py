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
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid


class UserProfileList(generics.ListCreateAPIView):
    """
    View for listing all user profiles and creating a new user profile.
    
    Handles GET requests to retrieve all user profiles and POST requests to create a new profile.
    Uses the UserProfileSerializer to serialize the data.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a specific user profile.

    Handles GET, PUT, PATCH, and DELETE requests for individual user profiles.
    Uses the UserProfileSerializer to serialize and deserialize the data.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    """
    View for handling user registration, including creating a new user and generating an authentication token.
    
    Accepts POST requests with user registration data (username, email, password), validates it,
    creates a new user, and returns an authentication token along with user details.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles the POST request to register a new user and issue an authentication token.
        """
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
    """
    View for handling user login and returning an authentication token.

    This view accepts user credentials (email and password), authenticates the user,
    and returns a token that can be used for authenticated API requests.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles the POST request to authenticate a user and issue an authentication token.
        """
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
@permission_classes([AllowAny])
def login_view(request):
    """
    View for user login that returns an access token and optionally sets a refresh token cookie.
    
    This view handles user login, generates a JWT access token, and optionally sets the refresh token as a cookie 
    (with a configurable expiration time based on 'remember me' choice).
    """
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
    """
    View for refreshing the access token using a valid refresh token stored in a cookie.
    
    This view reads the refresh token from the request cookies, validates it, and returns a new access token.
    """
    refresh_token = request.COOKIES.get("refreshToken")

    if not refresh_token:
        return JsonResponse({"error": "No refresh token"}, status=401)

    try:
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        return JsonResponse({"accessToken": access_token})
    except Exception:
        return JsonResponse({"error": "Invalid refresh token"}, status=401)


@csrf_exempt
def logout_view(request):
    """
    View for logging out the user by deleting the refresh token cookie.
    
    This view removes the 'refreshToken' cookie, effectively logging out the user and invalidating their session.
    """
    response = JsonResponse({"message": "Logged out"})
    response.delete_cookie("refreshToken")
    return response


class GuestLoginView(APIView):
    """
    API endpoint for guest login.

    This view creates a temporary guest user with a unique username and 
    generates JSON Web Tokens (JWT) for authentication.

    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        guest_id = uuid.uuid4().hex  # create unique ID for guest
        guest_user = User.objects.create_user(
            username=f"guest_{guest_id}",
            email=None,
            password=None
        )
        guest_user.save()

        # Generiere ein JWT für den Gast
        refresh = RefreshToken.for_user(guest_user)
        access_token = refresh.access_token

        return Response({
            'refreshToken': str(refresh),
            'accessToken': str(access_token),
            'guest_id': guest_id
        })


class GuestLogoutView(APIView):
    """
    API endpoint for guest logout.

    This view invalidates the provided refresh token and deletes the guest user if it exists.

    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refreshToken')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                user = User.objects.get(id=token["user_id"])
                user.delete()
                token.blacklist()

                return Response({"message": "Guest logged out and removed"}, status=200)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            except Exception:
                return Response({"error": "Invalid token"}, status=400)

        return Response({"message": "No active guest session"}, status=400)
