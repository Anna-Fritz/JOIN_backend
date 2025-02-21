from django.contrib import admin
from .models import User, Category, Prio, Subtask, Task

# Register your models here.

admin.site.register([User, Category, Prio, Subtask, Task])
