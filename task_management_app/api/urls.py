from django.contrib import admin
from django.urls import path
from .views import UsersView, UserSingleView, TasksView, TaskSingleView, SubtasksView, \
    SubtasksDoneView

urlpatterns = [
    path('user/', UsersView.as_view()),
    path('user/<int:pk>/', UserSingleView.as_view()),
    path('task/', TasksView.as_view()),
    path('task/<int:pk>/', TaskSingleView.as_view()),
    path('task/<int:pk>/subtask/', SubtasksView.as_view()),
    path('task/<int:pk>/subtask-done/', SubtasksDoneView.as_view())

]