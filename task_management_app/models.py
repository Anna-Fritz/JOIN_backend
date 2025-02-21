from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    contactNumber = models.CharField(max_length=30)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=15)
    color = models.CharField(max_length=7)

    def __str__(self):
        return self.name


class Prio(models.Model):
    level = models.CharField(max_length=15)
    icon_path = models.CharField(max_length=255)

    def __str__(self):
        return self.level


class Task(models.Model):
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
    subtask = models.CharField(max_length=255)
    task = models.ForeignKey(Task, related_name="subtasks", on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.subtask
