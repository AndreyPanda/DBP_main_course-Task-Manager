from base import TestViewSetBase
from http import HTTPStatus
from main.models.user import User


class TestUserViewSet(TestViewSetBase):
    basename = "users"
    user_attributes = {
        'username': 'johnsmit',
        'first_name': 'John',
        'last_name': 'Smith',
        'email': 'john@test.com',
        'role': 'developer',
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        attributes.pop('username')
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        user = self.create(self.user_attributes)
        print(f'user = {user}')
        expected_response = self.expected_details(user, self.user_attributes)
        print(f'expected_response = {expected_response}')
        assert user == expected_response

    def test_list(self):
        user_2_attributes = {
            "first_name": "Test-admin",
            "last_name": "Test-admin",
            "email": "test-admin@test.com",
            "role": 'admin',
        }
        user_2 = self.create_api_user(user_2_attributes)
        user_2_attributes["id"] = user_2.id

        response = self.list()
        self.user_attributes['id'] = self.user.id
        expected_response = [self.user_attributes, user_2_attributes]

        assert response.status_code == HTTPStatus.OK, response.content
        print(f'response.json = {response}')
        print(f'expected_response = {expected_response}')
        assert response.json() == expected_response

    # def test_retrieve(self):
    #     response = self.retrieve(key=self.user_attributes["id"])
    #     assert response.json() == self.user_attributes
    #
    # def test_update(self):
    #     data = self.user_attributes.copy()
    #     data["username"] = "test-manager"
    #     data["role"] = User.Roles.MANAGER
    #     del data["id"]
    #     another_user = self.create_api_user(data)
    #
    #     response = self.update(
    #         key=another_user.id,
    #         data={"first_name": "Test-admin-updated", "role": "developer"},
    #     )
    #
    #     assert response.status_code == HTTPStatus.FORBIDDEN, response.content
    #
    #     response = self.update(key=another_user.id, data={"role": "developer"})
    #
    #     assert response.status_code == HTTPStatus.OK, response.content
    #     assert response.json() == {"role": "developer"}
    #
    # def test_delete(self):
    #     another_user_attributes = {
    #         "username": "Test-manager",
    #         "first_name": "Test-manager",
    #         "last_name": "Test-manager",
    #         "email": "test-manager@test.com",
    #         "role": User.Roles.MANAGER,
    #     }
    #     another_user = self.create_api_user(another_user_attributes)
    #     id = another_user.id
    #
    #     response = self.delete(key=id)
    #     response_list = self.list()
    #     expected_response_list = [self.user_attributes]
    #
    #     assert response.status_code == HTTPStatus.NO_CONTENT, response.content
    #     assert response_list.json() == expected_response_list
