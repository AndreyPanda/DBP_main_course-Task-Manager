from main.models import User
from rest_framework.test import APIClient, APITestCase
from typing import Union, List
from django.urls import reverse
from http import HTTPStatus


class TestViewSetBase(APITestCase):
    # user: User = None
    # client: APIClient = None
    # basename: str

    @staticmethod
    def create_api_user(user_attributes):
        return User.objects.create(**user_attributes)

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        if cls.user_attributes:
            cls.user = cls.create_api_user(cls.user_attributes)
        else:
            cls.user = None
        cls.client = APIClient()

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[key])

    @classmethod
    def list_url(cls, args: List[Union[str, int]] = None) -> str:
        return reverse(f"{cls.basename}-list", args=args)

    def create(self, data: dict, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.post(self.list_url(args), data=data)
        assert response.status_code == HTTPStatus.CREATED, response.content
        return response.data

    def list(self, args: List[Union[str, int]] = None) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.list_url(args))
        return response

    def retrieve(self, key: Union[int, str]) -> dict:
        self.client.force_login(self.user)
        response = self.client.get(self.detail_url(key))
        return response

    def update(self, key: Union[int, str], data: dict) -> dict:
        self.client.force_login(self.user)
        response = self.client.put(self.detail_url(key), data=data)
        return response
