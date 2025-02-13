from django.db import models

# Create your models here.


class User (models.Model):
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    contactNumber = models.IntegerField()
    color = models.CharField(max_length=7)


class AssignedUser(models.Model):
    username = models.CharField(max_length=30)
    initials = models.CharField(max_length=2)
    color = models.CharField(max_length=7)


class Category(models.Model):
    name = models.CharField(max_length=15)
    color = models.CharField(max_length=7)


class Prio(models.Model):
    level = models.CharField(max_length=15)
    icon_path = models.CharField(max_length=255)


class Subtask(models.Model):
    checkbox_img = models.CharField(max_length=255)
    subtask = models.CharField(max_length=255)


class SubtaskDone(models.Model):
    subtask_done = models.CharField(max_length=255)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=255)
    assigned_users = models.ManyToManyField(AssignedUser)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    prio = models.ForeignKey(Prio, on_delete=models.CASCADE)
    subtasks = models.ManyToManyField(Subtask)
    subtasks_done = models.ManyToManyField(SubtaskDone)


class Summary(models.Model):
    todo_count = models.IntegerField()
    done_count = models.IntegerField()
    urgent_count = models.IntegerField()
    most_urgent_due_date = models.DateField()
    total_tasks = models.IntegerField()
    in_progress_count = models.IntegerField()
    awaiting_feedback_count = models.IntegerField()
