from main.models import User, Task, Tag
from rest_framework.test import APIClient, APITestCase
from typing import Union, List
from django.urls import reverse
from http import HTTPStatus
from rest_framework.response import Response


class TestViewSetBase(APITestCase):
    user: User = None
    client: APIClient = None
    basename: str

    setup_user_attributes = {
        "username": "johnsmit",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
        "avatar_picture": "picture.jpeg",
    }

    @staticmethod
    def create_api_user(user_attributes):
        return User.objects.create(**user_attributes)

    @staticmethod
    def create_task(task_attributes):
        return Task.objects.create(**task_attributes)

    @staticmethod
    def create_tag(tag_attributes):
        return Tag.objects.create(**tag_attributes)

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.user = cls.create_api_user(cls.setup_user_attributes)
        cls.client = APIClient()

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    @classmethod
    def list_url_filter(cls, filter_field: str = None, filter_value: str = None) -> str:
        url = reverse(f"{cls.basename}-list")
        return f"{url}?{filter_field}={filter_value}"

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url(args))
        return response

    def retrieve(self, key: Union[int, str]) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.detail_url(key))
        return response

    def update(self, key: Union[int, str], data: dict) -> dict:
        self.client.force_authenticate(self.user)
        response = self.client.put(self.detail_url(key), data=data)
        return response

    def delete(self, key: Union[int, str]) -> None:
        self.client.force_authenticate(self.user)
        response = self.client.delete(self.detail_url(key))
        return response

    def unauthenticated_request(self):
        self.client.logout()
        response = self.client.get(self.list_url())
        return response

    def filter(self, filter_field: str = None, filter_value: str = None) -> list:
        self.client.force_authenticate(self.user)
        response = self.client.get(self.list_url_filter(filter_field, filter_value))
        assert response.status_code == HTTPStatus.OK, response.content
        return response.json()

    def request_single_resource(self, data: dict = None) -> Response:
        self.client.force_authenticate(user=self.user, token=None)
        return self.client.get(self.list_url(), data=data)

    def single_resource(self, data: dict = None) -> dict:
        response = self.request_single_resource(data)
        assert response.status_code == HTTPStatus.OK
        return response.data

    def request_patch_single_resource(self, attributes: dict) -> Response:
        self.client.force_authenticate(user=self.user, token=None)
        url = self.list_url()
        return self.client.patch(url, data=attributes)

    def patch_single_resource(self, attributes: dict) -> dict:
        response = self.request_patch_single_resource(attributes)
        assert response.status_code == HTTPStatus.OK, response.content
        return response.data

    def get_expected_task_attr(cls, task: Task) -> dict:
        tag_list = [tag.title for tag in task.tags.all()]
        expected_task_attr = {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "deadline": task.deadline
            if isinstance(task.deadline, str)
            else task.deadline.strftime("%Y-%m-%d"),
            "executor": task.executor.id,
            "date_of_creation": task.date_of_creation
            if isinstance(task.date_of_creation, str)
            else task.date_of_creation.strftime("%Y-%m-%d"),
            "date_of_change": None,
            "tags": tag_list,
            "state": str(task.state),
            "priority": task.priority,
        }
        return expected_task_attr

    @classmethod
    def get_expected_tag_attr(cls, tag: Tag) -> dict:
        return {
            "id": tag.id,
            "title": tag.title,
        }
