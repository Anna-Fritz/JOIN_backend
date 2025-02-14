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


class SubtaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        """Filtert die Subtask-Liste so, dass nur Subtasks der spezifischen Task zurückgegeben werden."""
        task_id = self.kwargs.get('task_id')  # Task-ID aus der URL holen
        return Subtask.objects.filter(task__id=task_id)  # Nur Subtasks der Task zurückgeben

    def perform_update(self, serializer):
        """Stellt sicher, dass die Subtask immer mit der richtigen Task verknüpft bleibt."""
        subtask = serializer.save()  # Subtask speichern
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        if subtask not in task.subtasks.all():
            task.subtasks.add(subtask)  # Falls sie nicht mehr verknüpft ist, wieder hinzufügen

    def perform_destroy(self, instance):
        """Entfernt die Subtask auch aus der ManyToMany-Beziehung der Task, bevor sie gelöscht wird."""
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        task.subtasks.remove(instance)  # Entfernt die Subtask aus der Task-Relation
        instance.delete()  # Löscht die Subtask endgültig


class SubtasksDoneView(generics.ListCreateAPIView):
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


class SubtaskDoneSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskDoneSerializer

    def get_queryset(self):
        """Filtert die Subtask-Liste so, dass nur Subtasks der spezifischen Task zurückgegeben werden."""
        task_id = self.kwargs.get('task_id')  # Task-ID aus der URL holen
        return SubtaskDone.objects.filter(task__id=task_id)  # Nur Subtasks der Task zurückgeben

    def perform_update(self, serializer):
        """Stellt sicher, dass die Subtask immer mit der richtigen Task verknüpft bleibt."""
        subtask_done = serializer.save()  # Subtask speichern
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        if subtask_done not in task.subtasks_done.all():
            task.subtasks_done.add(subtask_done)  # Falls sie nicht mehr verknüpft ist, wieder hinzufügen

    def perform_destroy(self, instance):
        """Entfernt die Subtask auch aus der ManyToMany-Beziehung der Task, bevor sie gelöscht wird."""
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        task.subtasks_done.remove(instance)  # Entfernt die Subtask aus der Task-Relation
        instance.delete()  # Löscht die Subtask_Done endgültig