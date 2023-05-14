from django.urls import reverse
from typing import Union
from base import TestViewSetBase
from main.models import User, Task
from factories import UserFactory
from http import HTTPStatus


class TestUserTasksViewSet(TestViewSetBase):
    basename = "user_tasks"
    user_attributes = UserFactory.build(role=User.Roles.ADMIN)

    @classmethod
    def detail_url(cls, key: Union[int, str]) -> str:
        return reverse(f"{cls.basename}-detail", args=[*key])

    def test_list(self) -> None:
        task_attributes = {
            "title": "One more task",
            "description": "To make a test",
            "deadline": "2023-05-30",
            "state": Task.States.NEW_TASK,
            "priority": Task.Priority.MEDIUM,
            "author": self.user,
            "executor": self.user,
        }
        task = self.create_task(task_attributes)
        response = self.list(args=[self.user.id])
        expected_response = [
            self.get_expected_task_attr(task),
        ]
        assert response.json() == expected_response

    def test_retrieve_foreign_task(self) -> None:
        second_user_attributes = UserFactory.build(role=User.Roles.ADMIN)
        second_user = self.create_api_user(second_user_attributes)
        task_attributes = {
            "title": "One more task",
            "description": "To make a test",
            "deadline": "2023-05-30",
            "state": Task.States.NEW_TASK,
            "priority": Task.Priority.MEDIUM,
            "author": self.user,
            "executor": second_user,
        }
        task = self.create_task(task_attributes)
        response = self.retrieve(key=[self.user.id, task.id])
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_retrieve(self) -> None:
        task_attributes = {
            "title": "One more task",
            "description": "To make a test",
            "deadline": "2023-05-30",
            "state": Task.States.NEW_TASK,
            "priority": Task.Priority.MEDIUM,
            "author": self.user,
            "executor": self.user,
        }
        task = self.create_task(task_attributes)
        expected_response = self.get_expected_task_attr(task)
        response = self.retrieve(key=[self.user.id, task.id])
        assert response.json() == expected_response
