from unittest.mock import patch, MagicMock

from django.core import mail
from django.template.loader import render_to_string

from main.models import Task, User
from main.services.mail import send_assign_notification
from base import TestViewSetBase


class TestSendEmail(TestViewSetBase):
    user_attributes = {
        "username": "AndreyPanda",
        "name": "Andrey",
        "surname": "Panda",
        "email": "lamoremio@gmail.com",
        "password": "anewpassword",
        "role": User.Roles.DEVELOPER,
    }

    @patch.object(mail, "send_mail")
    def test_send_assign_notification(self, fake_sender: MagicMock) -> None:
        assignee = self.user

        task_data = {
            "title": "A task to check the emails service",
            "description": "Please check the function",
            "deadline": "2023-06-01",
            "state": Task.States.NEW_TASK,
            "priority": Task.Priority.MEDIUM,
            "author": self.user,
            "executor": assignee,
        }

        task = self.create_task(task_data)

        send_assign_notification(task.id)

        fake_sender.assert_called_once_with(
            subject="You've assigned a task.",
            message="",
            from_email=None,
            recipient_list=[assignee.email],
            html_message=render_to_string(
                "emails/notification.html",
                context={"task": Task.objects.get(pk=task.id)},
            ),
        )
