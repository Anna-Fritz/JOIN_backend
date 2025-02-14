from rest_framework import serializers
from ..models import User, AssignedUser, Category, Prio, Subtask, SubtaskDone, Summary, Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ['id']


class CategorySerialzer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class PrioSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Prio
        exclude = ['id']


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
    prio = PrioSerialzer(read_only=True)
    prio_id = serializers.PrimaryKeyRelatedField(
        queryset=Prio.objects.all(),
        write_only=True,
        source='prio'
    )

    class Meta:
        model = Task
        fields = "__all__"
