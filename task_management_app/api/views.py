from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from ..models import User, Task, Subtask, SubtaskDone
from .serializers import UserSerializer, TaskSerializer, SubtaskSerializer, SubtaskDoneSerializer


class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubtasksView(generics.ListCreateAPIView):
    # queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        return task.subtasks.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        subtask = serializer.save()
        task.subtasks.add(subtask)


class SubtasksDoneView(generics.ListCreateAPIView):
    # queryset = SubtaskDone.objects.all()
    serializer_class = SubtaskDoneSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        return task.subtasks_done.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        subtask_done = serializer.save()
        task.subtasks_done.add(subtask_done)
