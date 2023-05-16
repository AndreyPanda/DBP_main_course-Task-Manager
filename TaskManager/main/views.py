from rest_framework import viewsets, mixins, status
from .serializers import UserSerializer, TaskSerializer, TagSerializer
from .models import User, Task, Tag
from django_filters import (
    FilterSet,
    CharFilter,
    ChoiceFilter,
    ModelMultipleChoiceFilter,
)
from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from typing import cast, Any
from rest_framework_extensions.mixins import NestedViewSetMixin
from rest_framework.reverse import reverse
from main.serializers import CountdownJobSerializer
from main.services.async_celery import AsyncJob, JobStatus
from rest_framework.request import Request
from rest_framework.response import Response
from django.http import Http404, HttpResponse


class UserFilter(FilterSet):
    username = CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class TaskFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")
    state = ChoiceFilter(choices=Task.States.choices)
    tags = ModelMultipleChoiceFilter(
        field_name="tags__title", queryset=Tag.objects.all()
    )
    author = CharFilter(field_name="user__username", lookup_expr="icontains")
    executor = CharFilter(field_name="user__username", lookup_expr="icontains")

    class Meta:
        model = Task
        fields = ("title", "state", "tags", "author", "executor")


class TagFilter(FilterSet):
    title = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("title",)


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
    filterset_class = TagFilter


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "executor")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TaskTagsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class CountdownJobViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = CountdownJobSerializer

    def get_success_headers(self, data: dict) -> dict[str, str]:
        task_id = data["task_id"]
        return {"Location": reverse("jobs-detail", args=[task_id])}


class AsyncJobViewSet(viewsets.GenericViewSet):
    serializer_class = JobSerializer

    def get_object(self) -> AsyncJob:
        lookup_url_kwargs = self.lookup_url_kwarg or self.lookup_field
        task_id = self.kwargs[lookup_url_kwargs]
        job = AsyncJob.from_id(task_id)
        if job.status == JobStatus.UNKNOWN:
            raise Http404()
        return job

    def retrieve(self, request: Request, *args: Any, **kwargs: Any) -> HttpResponse:
        instance = self.get_object()
        serializer_data = self.get_serializer(instance).data
        if instance.status == JobStatus.SUCCESS:
            location = self.request.build_absolute_uri(instance.result)
            return Response(
                serializer_data,
                headers={"location": location},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer_data)
