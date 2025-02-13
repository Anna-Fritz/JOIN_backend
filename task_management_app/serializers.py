from rest_framework import serializers
from .models import User, AssignedUser, Category, Prio, Subtask, SubtaskDone, Summary, Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
