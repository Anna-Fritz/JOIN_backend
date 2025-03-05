from django.urls import path
from .views import UserProfileList, UserProfileDetail, RegistrationView, LoginView, login_view, refresh_view, logout_view

urlpatterns = [
    path('profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('login/', login_view, name='login'),
    path('login/refresh/', refresh_view, name='refresh'),
    path('logout/', logout_view, name='logout'),
    # path('login/', LoginView.as_view(), name='login')
]
