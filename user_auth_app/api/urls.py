from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, login_view, refresh_view, logout_view, GuestLoginView, GuestLogoutView

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
    path('login/refresh/', refresh_view, name='refresh'),
    path('login/guest/', GuestLoginView.as_view(), name="guest-login"),
    path('logout/', logout_view, name='logout'),
    path('logout/guest/', GuestLogoutView.as_view(), name="guest-logout")
]
