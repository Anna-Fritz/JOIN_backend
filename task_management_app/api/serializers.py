from rest_framework import serializers
from ..models import User, Category, Prio, Subtask, Task


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PrioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prio
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class SubtaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subtask
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
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        write_only=True,
        source='category'
    )
    prio = PrioSerializer(read_only=True)
    prio_id = serializers.PrimaryKeyRelatedField(
        queryset=Prio.objects.all(),
        write_only=True,
        source='prio'
    )
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'assigned_users', 'assigned_user_id', 'due_date', 'prio', 'prio_id', 'category', 'category_id', 'status', 'subtasks']

    def create(self, validated_data):
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_users = validated_data.pop('assigned_users', [])
        task = Task.objects.create(**validated_data)
        task.assigned_users.set(assigned_users)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.prio = validated_data.get('prio', instance.prio)
        instance.category = validated_data.get('category', instance.category)
        instance.status = validated_data.get('status', instance.status)

        if 'assigned_users' in validated_data:
            instance.assigned_users.set(validated_data['assigned_users'])

        if 'subtasks' in validated_data:
            instance.subtasks.all().delete()
            for subtask_data in validated_data['subtasks']:
                Subtask.objects.create(task=instance, **subtask_data)

        instance.save()
        return instance
    
