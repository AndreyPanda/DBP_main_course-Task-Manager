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

    # def test_list(self):
    #     user_2_attributes = {
    #         'first_name': 'Ivan',
    #         'last_name': 'Ivanov',
    #         'email': 'test-admin@test.com',
    #         'role': 'admin',
    #     }
    #     user_2 = self.create_api_user(user_2_attributes)
    #     user_2_attributes['id'] = user_2.id
    #
    #     response = self.list()
    #     self.user_attributes['id'] = self.user.id
    #     expected_response = [self.user_attributes, user_2_attributes]
    #
    #     assert response.status_code == HTTPStatus.OK, response.content
    #     assert response.json() == expected_response
    #
    # def test_retrieve(self):
    #     response = self.retrieve(key=self.user_attributes['id'])
    #     assert response.json() == self.user_attributes
    #
    # def test_update(self):
    #     data = self.user_attributes.copy()
    #     data['first_name'] = 'Maria'
    #     del data['id']
    #
    #     response = self.update(
    #         key=self.user.id,
    #         data=data,
    #     )
    #
    #     assert response.status_code == HTTPStatus.OK, response.content
    #     assert response.json()['first_name'] == 'Maria'
    #
    # def test_delete(self):
    #     some_user_attributes = {
    #         'first_name': 'Godzilla',
    #         'last_name': 'Petrov',
    #         'email': 'godzilla@gmail.com',
    #         'role': 'manager',
    #     }
    #     some_user = self.create_api_user(some_user_attributes)
    #
    #     response = self.delete(key=some_user.id)
    #     response_list = self.list()
    #     self.user_attributes['id'] = self.user.id
    #     expected_response_list = [self.user_attributes]
    #
    #     assert response.status_code == HTTPStatus.NO_CONTENT, response.content
    #     assert response_list.json() == expected_response_list
