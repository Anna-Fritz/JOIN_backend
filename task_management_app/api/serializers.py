from rest_framework import serializers
from ..models import User, AssignedUser, Category, Prio, Subtask, SubtaskDone, Summary, Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class CategorySerialzer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    assigned_users = UserSerializer(many=True, read_only=True)
    assigned_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='assigned_users'
    )
    category = CategorySerialzer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )

    class Meta:
        model = Task
        fields = "__all__"
