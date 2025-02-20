from rest_framework import serializers
from ..models import User, Category, Prio, Subtask, SubtaskDone, Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PrioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prio
        fields = "__all__"


class CategorySerialzer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class PrioSerialzer(serializers.ModelSerializer):

    class Meta:
        model = Prio
        exclude = ['id']


class SubtaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
        fields = "__all__"


class SubtaskDoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubtaskDone
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):

    assigned_users = UserSerializer(many=True, read_only=True)
    assigned_user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        required=False,
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
    subtasks = SubtaskSerializer(many=True, read_only=True)
    subtask_id = serializers.PrimaryKeyRelatedField(
        queryset=Subtask.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='subtasks'
    )
    subtasks_done = SubtaskDoneSerializer(many=True, read_only=True)
    subtask_done_id = serializers.PrimaryKeyRelatedField(
        queryset=SubtaskDone.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='subtasks_done'
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_users', 'assigned_user_id', 'due_date', 'prio', 'prio_id', 'category', 'category_id', 'status', 'subtasks', 'subtask_id', 'subtasks_done', 'subtask_done_id']

