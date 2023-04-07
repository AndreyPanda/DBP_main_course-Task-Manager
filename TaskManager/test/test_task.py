from base import TestViewSetBase
from http import HTTPStatus
import base
from main.models import User, Task, Tag
from rest_framework.test import APIClient
from datetime import date


class TestTaskViewSet(TestViewSetBase):
    basename = 'tasks'
    tag_attributes = {
        'title': 'asap'
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, 'id': entity['id']}

    def test_create(self):
        tag = TestViewSetBase.create_tag(self.tag_attributes)
        task_attributes = {
            'title': 'first_task',
            'description': 'Implement API tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task = self.create(task_attributes)
        expected_response = self.expected_details({'id': task['id']}, task_attributes)
        assert task == expected_response

    def test_list(self):
        tag = TestViewSetBase.create_tag(self.tag_attributes)
        task_attributes = {
            'title': 'first_task',
            'description': 'Implement API tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task_2_attributes = {
            'title': 'second_task',
            'description': 'Implement another tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task = self.create(task_attributes)
        task_2 = self.create(task_2_attributes)
        response = self.list()
        expected_response = [
            self.expected_details({'id': task['id']}, task_attributes),
            self.expected_details({'id': task_2['id']}, task_2_attributes),
        ]
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        tag = TestViewSetBase.create_tag(self.tag_attributes)
        task_attributes = {
            'title': 'first_task',
            'description': 'Implement API tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task = self.create(task_attributes)
        response = self.retrieve(key=task['id'])
        assert response.json() == self.expected_details({'id': task['id']}, task_attributes)

    def test_update(self):
        tag = TestViewSetBase.create_tag(self.tag_attributes)
        task_attributes = {
            'title': 'first_task',
            'description': 'Implement API tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task = self.create(task_attributes)
        task_attributes['title'] = 'To build a new structure'
        response = self.update(
            key=task['id'],
            data=task_attributes,
        )
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json()['title'] == 'To build a new structure'

    def test_delete(self):
        tag = TestViewSetBase.create_tag(self.tag_attributes)
        task_attributes = {
            'title': 'first_task',
            'description': 'Implement API tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task = self.create(task_attributes)
        response = self.delete(key=task['id'])
        response_list = self.list()
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list.json() == []

    def test_unauthenticated_request(self):
        response = self.unauthenticated_request()
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_filter(self):
        tag = TestViewSetBase.create_tag(self.tag_attributes)
        task_attributes = {
            'title': 'first_task',
            'description': 'Implement API tests',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task_2_attributes = {
            'title': 'To build a new structure',
            'description': 'To build a new structure',
            'tags': [tag.id],
            'date_of_creation': date.today().isoformat(),
            'date_of_change': '2023-04-07',
            'deadline': '2023-04-20',
            'state': Task.States.NEW_TASK,
            'priority': Task.Priority.MEDIUM,
            'executor': User.objects.first().id,
        }
        task = self.create(task_attributes)
        task_2 = self.create(task_2_attributes)

        filter_field = 'title'
        filter_value = 'build'
        tasks = self.list().json()
        expected_tasks: list = []
        for task in tasks:
            if filter_value in task[filter_field]:
                expected_tasks.append(task)
                break
        response = self.filter(filter_field=filter_field, filter_value=filter_value)
        print(f'response = {response}')
        print(f'expected_tasks = {expected_tasks}')
        assert response == expected_tasks
