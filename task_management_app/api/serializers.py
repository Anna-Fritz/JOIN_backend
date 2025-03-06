from rest_framework import serializers
from ..models import User, Category, Prio, Subtask, Task


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    Handles the transformation of User model instances into JSON format
    and vice versa.
    """
    class Meta:
        model = User
        fields = "__all__"


class PrioSerializer(serializers.ModelSerializer):
    """
    Serializer for the Prio model.

    Converts Prio model instances to and from JSON. The `level` and 
    `icon_path` fields are included in the serialized data.
    """
    class Meta:
        model = Prio
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.

    Transforms Category model instances into JSON format and vice versa.
    The `name` and `color` fields are included in the serialized data.
    """
    class Meta:
        model = Category
        fields = "__all__"


class SubtaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Subtask model.

    Responsible for serializing Subtask instances, which represent tasks 
    that are part of a larger task. Includes fields like `subtask` and 
    `completed`.
    """
    class Meta:
        model = Subtask
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    This serializer handles the serialization of task-related data, including:
    - Basic task attributes like `title`, `description`, `due_date`, and `status`
    - Associated users, categories, priorities, and subtasks.

    Custom methods `create()` and `update()` are implemented to handle 
    complex relationships such as assigned users and subtasks.
    """
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
        """
        Custom create method to handle the creation of a Task along with
        its associated users and subtasks.

        Extracts and handles the `assigned_users` and `subtasks` data 
        separately from the main task data to ensure proper relationships.
        """
        subtasks_data = validated_data.pop('subtasks', [])
        assigned_users = validated_data.pop('assigned_users', [])
        task = Task.objects.create(**validated_data)
        task.assigned_users.set(assigned_users)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)
        return task
    
    def update(self, instance, validated_data):
        """
        Custom update method to handle updates to a Task instance, 
        including the modification of its associated users and subtasks.

        Ensures that the related `assigned_users` and `subtasks` are 
        properly updated when the task is modified.
        """
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
    
