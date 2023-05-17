from main.models import User, Task
from base import TestViewSetBase
from factories import UserFactory


class TestUserTasksViewSet(TestViewSetBase):
    basename = "task_tags"
    user_attributes = UserFactory.build(role=User.Roles.ADMIN)

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

        tag_attributes = {"title": "a first tag"}
        tag = self.create_tag(tag_attributes)
        tag_2_attributes = {"title": "a second tag"}
        tag_2 = self.create_tag(tag_2_attributes)
        self.add_tags(task, [tag, tag_2])
        tags = self.list(args=[task.id])
        assert tags.json() == [
            self.get_expected_tag_attr(tag),
            self.get_expected_tag_attr(tag_2),
        ]

    def add_tags(self, task: dict, tags: list) -> None:
        task_instance = Task.objects.get(pk=task.id)
        task_instance.tags.add(*tags)
        task_instance.save()
