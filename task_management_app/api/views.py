from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from ..models import User, Task, Subtask, Prio, Category
from .serializers import UserSerializer, TaskSerializer, SubtaskSerializer, \
    PrioSerializer, CategorySerializer
from django.db.models import Count, Min, Q


class UsersView(generics.ListCreateAPIView):
    """
    View for listing all users and creating a new user.

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single user.

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PriosView(generics.ListCreateAPIView):
    """
    View for listing all priorities and creating a new priority.

    """
    queryset = Prio.objects.all()
    serializer_class = PrioSerializer


class CategoriesView(generics.ListCreateAPIView):
    """
    View for listing all categories and creating a new category.

    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TasksView(generics.ListCreateAPIView):
    """
    View for listing all tasks and creating a new task.

    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class TaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single task.

    This view handles operations on a single task, including retrieving
    task details, updating task information, and deleting a task record.
    It uses the TaskSerializer for serializing task data.
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class SubtasksView(generics.ListCreateAPIView):
    """
    View for listing and creating subtasks related to a specific task.

    This view handles the retrieval of all subtasks for a specific task,
    as well as the creation of new subtasks. The task is identified by its `pk`.
    """
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        """
        Returns the subtasks related to a specific task.

        The `pk` of the task is retrieved from the URL and used to filter
        the related subtasks.
        """
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        return task.subtasks.all()

    def perform_create(self, serializer):
        """
        Creates a new subtask and links it to the correct task.

        The subtask is added to the ManyToMany relation between the task
        and subtasks if it isn't already associated with the task.
        """
        pk = self.kwargs.get('pk')
        task = Task.objects.get(pk=pk)
        subtask = serializer.save()

        if subtask not in task.subtasks.all():
            task.subtasks.add(subtask)


class SubtaskSingleView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting a single subtask.

    This view handles operations on a single subtask, including retrieving
    subtask details, updating subtask information, and deleting a subtask.
    The subtask is always linked to a specific task.
    """
    serializer_class = SubtaskSerializer

    def get_queryset(self):
        """
        Filters the subtask list so that only subtasks of the specific task
        are returned.

        The `task_id` is retrieved from the URL to ensure only subtasks
        belonging to that task are included.
        """
        task_id = self.kwargs.get('task_id')
        return Subtask.objects.filter(task__id=task_id)

    def perform_update(self, serializer):
        """
        Ensures that the subtask always remains linked to the correct task.

        This method ensures that the subtask is saved and remains part of
        the specified task. If the subtask is not already associated with the
        task, it is added back to the task's subtasks.
        """
        subtask = serializer.save(partial=True)  # save subtask
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        if subtask not in task.subtasks.all():
            task.subtasks.add(subtask)  # If it is no longer linked, add it back

    def perform_destroy(self, instance):
        """
        Removes the subtask from the task's ManyToMany relationship before deleting it.

        This method removes the subtask from the task's relationship before
        permanently deleting it from the database.
        """
        task_id = self.kwargs.get('task_id')
        task = Task.objects.get(id=task_id)

        task.subtasks.remove(instance)  # remove subtask of task relation
        instance.delete()  # deletes subtask permanently


class SummaryView(APIView):
    """
    View for retrieving a summary of task statistics.

    This view aggregates task data and returns key statistics, such as:
    - The number of tasks in various states (e.g., `to_do`, `done`)
    - The total number of tasks
    - The most urgent task's due date
    - Tasks filtered by priority level
    """

    def get(self, request):
        """
        Retrieves a summary of task statistics.

        This method calculates counts of tasks based on their `status` and 
        `prio` level and returns aggregated data, including counts for
        `to_do`, `done`, `in_progress`, `await_feedback`, and `urgent` tasks.
        """
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
