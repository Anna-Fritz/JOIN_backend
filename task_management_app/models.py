from django.db import models

# Create your models here.


class User(models.Model):
    """
    Represents a user in the system with essential contact details.

    """
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    contactNumber = models.CharField(max_length=30)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.username


class Category(models.Model):
    """
    Represents a category for organizing tasks.

    """
    name = models.CharField(max_length=15, unique=True)
    color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.name


class Prio(models.Model):
    """
    Represents the priority level of a task.

    """
    level = models.CharField(max_length=15)
    icon_path = models.CharField(max_length=255)

    def __str__(self):
        return self.level


class Task(models.Model):
    """
    Represents a task to be completed with various attributes and assigned users.

    Attributes:
    title (str): The title or name of the task.
    description (str): A detailed description of the task (optional).
    due_date (date): The due date for the task.
    status (str): The current status of the task (e.g., "to_do", "in_progress").
    assigned_users (ManyToManyField): A list of users assigned to the task.
    category (ForeignKey): The category the task belongs to.
    prio (ForeignKey): The priority level of the task.

    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=255, default="to_do")
    assigned_users = models.ManyToManyField(User, related_name='tasks', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prio = models.ForeignKey(Prio, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Subtask(models.Model):
    """
    Represents a subtask that belongs to a parent task.

    """
    subtask = models.CharField(max_length=255)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.subtask
