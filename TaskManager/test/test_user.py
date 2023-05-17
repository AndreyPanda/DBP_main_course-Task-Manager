from base import TestViewSetBase
from http import HTTPStatus
from factories import UserFactory, LargeAvatarUserFactory
import factory


class TestUserViewSet(TestViewSetBase):
    basename = "users"

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        try:
            attributes.pop("password")
        except:
            pass
        return {
            **attributes,
            "id": entity["id"],
            "avatar_picture": entity["avatar_picture"],
            "role": entity["role"],
        }

    def test_create(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user = self.create(user_attributes)
        expected_response = self.expected_details(user, user_attributes)
        assert user == expected_response

    def test_list(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_2 = self.create(user_attributes)
        response = self.list()
        response_list = response.json()
        expected_response = [
            self.expected_details(response_list[0], self.setup_user_attributes),
            self.expected_details(response_list[1], user_attributes),
        ]
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        response = self.retrieve(key=self.user.id)
        assert response.json() == self.expected_details(
            response.json(), self.setup_user_attributes
        )

    def test_update(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        data = user_attributes.copy()
        data["first_name"] = "Maria"
        response = self.update(
            key=self.user.id,
            data=data,
        )
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json()["first_name"] == "Maria"

    def test_delete(self):
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        some_user = self.create(user_attributes)
        response = self.delete(key=some_user["id"])
        response_list = self.list().json()
        expected_response_list = self.expected_details(
            response_list[0], self.setup_user_attributes
        )
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list == [expected_response_list]

    def test_unauthenticated_request(self):
        response = self.unauthenticated_request()
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_filter(self):
        filter_field = "username"
        filter_value = "a"
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_for_filter = self.create(user_attributes)
        users = self.list().json()
        expected_users: list = []
        for user in users:
            if filter_value in user[filter_field]:
                expected_users.append(user)
                break
        response = self.filter(filter_field=filter_field, filter_value=filter_value)
        assert response == expected_users

    def test_large_avatar(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = factory.build(dict, FACTORY_CLASS=LargeAvatarUserFactory)
        response = self.client.post(
            self.list_url(), data=user_attributes, format="multipart"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {"avatar_picture": ["Maximum size 1048576 exceeded."]}

    def test_avatar_bad_extension(self) -> None:
        self.client.force_authenticate(self.user)
        user_attributes = factory.build(dict, FACTORY_CLASS=UserFactory)
        user_attributes["avatar_picture"].name = "bad_extension.pdf"
        response = self.client.post(
            self.list_url(), data=user_attributes, format="multipart"
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json() == {
            "avatar_picture": [
                "File extension “pdf” is not allowed. Allowed extensions are: jpeg, jpg, png."
            ]
        }
