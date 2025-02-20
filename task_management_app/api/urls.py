from django.contrib import admin
from django.urls import path
from .views import UsersView, UserSingleView, TasksView, TaskSingleView, SubtasksView, \
    SubtasksDoneView, SubtaskSingleView, SubtaskDoneSingleView, SummaryView, PriosView

urlpatterns = [
    path('user/', UsersView.as_view()),
    path('user/<int:pk>/', UserSingleView.as_view()),
    path('task/', TasksView.as_view()),
    path('task/<int:pk>/', TaskSingleView.as_view()),
    path('task/<int:pk>/subtask/', SubtasksView.as_view()),
    path('task/<int:task_id>/subtask/<int:pk>/', SubtaskSingleView.as_view(), name='subtask-detail'),
    path('task/<int:pk>/subtask-done/', SubtasksDoneView.as_view()),
    path('task/<int:task_id>/subtask-done/<int:pk>/', SubtaskDoneSingleView.as_view(), name='subtask-done-detail'),
    path('summary/', SummaryView.as_view()),
    path('prio/', PriosView.as_view())
]