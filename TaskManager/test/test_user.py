from base import TestViewSetBase
from http import HTTPStatus


class TestUserViewSet(TestViewSetBase):
    basename = 'users'
    user_attributes = {
        'username': 'johnsmitagain',
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john@test.com',
        'role': 'developer',
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, 'id': entity['id']}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_list(self):
        user_2 = self.create_api_user(self.user_attributes)
        response = self.list()
        expected_response = [
            self.expected_details({'id': self.user.id}, self.setup_user_attributes),
            self.expected_details({'id': user_2.id}, self.user_attributes),
        ]
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user.id)
        assert response.json() == self.expected_details({'id': self.user.id}, self.setup_user_attributes)

    def test_update(self):
        data = self.user_attributes.copy()
        data['first_name'] = 'Maria'
        response = self.update(
            key=self.user.id,
            data=data,
        )
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json()['first_name'] == 'Maria'

    def test_delete(self):
        some_user = self.create_api_user(self.user_attributes)
        response = self.delete(key=some_user.id)
        response_list = self.list()
        expected_response_list = self.expected_details({'id': self.user.id}, self.setup_user_attributes)
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list.json() == [expected_response_list]
