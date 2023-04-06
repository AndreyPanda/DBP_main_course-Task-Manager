from rest_framework import viewsets
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .models import User, Task, Tag
from django_filters import (
    FilterSet,
    CharFilter,
    ChoiceFilter,
    ModelMultipleChoiceFilter,
)


class UserFilter(FilterSet):
    username = CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class TaskFilter(FilterSet):
    state = ChoiceFilter(choices=Task.States.choices)
    tags = ModelMultipleChoiceFilter(
        field_name="tags__title", queryset=Tag.objects.all()
    )
    author = CharFilter(field_name="user__username", lookup_expr="icontains")
    executor = CharFilter(field_name="user__username", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ("state", "tags", "author", "executor")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
