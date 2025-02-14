from django.contrib import admin
from django.urls import path
from .views import UsersView, UserSingleView, TasksView

urlpatterns = [
    path('user/', UsersView.as_view()),
    path('user/<int:pk>/', UserSingleView.as_view()),
    path('task/', TasksView.as_view())

]