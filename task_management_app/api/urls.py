from django.contrib import admin
from django.urls import path
from .views import UsersView, UserSingleView, TasksView, TaskSingleView, SubtasksView, \
    SubtaskSingleView, SummaryView, PriosView, CategoriesView

urlpatterns = [
    path('user/', UsersView.as_view(), name="user-list"),
    path('user/<int:pk>/', UserSingleView.as_view(), name="user-detail"),
    path('task/', TasksView.as_view(), name="task-list"),
    path('task/<int:pk>/', TaskSingleView.as_view(), name="task-detail"),
    path('task/<int:pk>/subtask/', SubtasksView.as_view(), name="subtask-list"),
    path('task/<int:task_id>/subtask/<int:pk>/', SubtaskSingleView.as_view(), name='subtask-detail'),
    path('summary/', SummaryView.as_view(), name="summary"),
    path('prio/', PriosView.as_view(), name="prio-list"),
    path('category/', CategoriesView.as_view(), name="category-list")
]
