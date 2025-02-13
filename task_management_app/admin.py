from django.contrib import admin
from .models import User, AssignedUser, Category, Prio, Subtask, SubtaskDone, Summary, Task

# Register your models here.

admin.site.register([User, AssignedUser, Category, Prio, Subtask, SubtaskDone, Summary, Task])