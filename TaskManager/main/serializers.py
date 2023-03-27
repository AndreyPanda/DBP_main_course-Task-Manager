from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email', 'date_of_birth',
            'phone'
        )

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "title",
        )

class TaskSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "date_of_creation",
            "date_of_change",
            "deadline",
            "state",
            "priority",
            "executor",
            "tags",
        ]