from django.contrib import admin
from .models import User, Category, Prio, Subtask, Task

# Register your models here.

# Registering models to the Django admin interface for management
admin.site.register([User, Category, Prio, Subtask, Task])
