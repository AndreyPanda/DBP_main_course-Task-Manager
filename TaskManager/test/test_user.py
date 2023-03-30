from base import TestViewSetBase
from http import HTTPStatus


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        "username": "johnsmit",
        "first_name": "John",
        "last_name": "Smith",
        "email": "john@test.com",
        "role": "developer",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        attributes.pop("username")
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        expected_response = self.expected_details(user, self.user_attributes)
        assert user == expected_response

    def test_list(self):
        user_2_attributes = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'email': 'test-admin@test.com',
            'role': 'admin',
        }
        user_2 = self.create_api_user(user_2_attributes)
        user_2_attributes["id"] = user_2.id

        response = self.list()
        self.user_attributes["id"] = self.user.id
        expected_response = [self.user_attributes, user_2_attributes]

        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response
