from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import User, Task, Subtask, Prio, Category
from .serializers import UserSerializer, TaskSerializer, SubtaskSerializer, \
    PrioSerializer, CategorySerializer
from django.db.models import Count, Min, Q


class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PriosView(generics.ListCreateAPIView):
    queryset = Prio.objects.all()
    serializer_class = PrioSerializer


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TasksView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]


class SubtasksView(generics.ListCreateAPIView):
    serializer_class = SubtaskSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        return task.subtasks.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        subtask = serializer.save()

        if subtask not in task.subtasks.all():
            task.subtasks.add(subtask)


class SubtaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        """Filters the subtask list so that only subtasks of the specific task are returned"""
        task_id = self.kwargs.get('task_id')  # get task_id of url
        return Subtask.objects.filter(task__id=task_id)  # return subtask only of the task

    def perform_update(self, serializer):
        """Ensures that the subtask always remains linked to the correct task"""
        subtask = serializer.save(partial=True)  # save subtask
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        if subtask not in task.subtasks.all():
            task.subtasks.add(subtask)  # If it is no longer linked, add it back

    def perform_destroy(self, instance):
        """Removes the subtask from the task's ManyToMany relationship before deleting it"""
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        task.subtasks.remove(instance)  # remove subtask of task relation
        instance.delete()  # deletes subtask permanently


class SummaryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        summary_data = Task.objects.aggregate(
            todo_count=Count("id", filter=Q(status="to_do")),
            done_count=Count("id", filter=Q(status="done")),
            total_tasks=Count("id"),
            urgent_count=Count("id", filter=Q(prio__level="urgent")),
            most_urgent_due_date=Min("due_date", filter=Q(prio__level="urgent")),
            in_progress_count=Count("id", filter=Q(status="in_progress")),
            awaiting_feedback_count=Count("id", filter=Q(status="await_feedback"))
        )

        return Response(summary_data)