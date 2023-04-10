from base import TestViewSetBase
from http import HTTPStatus


class TestTaskViewSet(TestViewSetBase):
    basename = "tags"
    tag_attributes = {
        "title": "asap",
    }

    @staticmethod
    def expected_details(entity: dict, attributes: dict):
        return {**attributes, "id": entity["id"]}

    def test_create(self):
        tag = TestViewSetBase.create(self, data=self.tag_attributes)
        expected_response = self.expected_details(
            {"id": tag["id"]}, self.tag_attributes
        )
        assert tag == expected_response

    def test_list(self):
        tag = TestViewSetBase.create(self, data=self.tag_attributes)
        tag_2_attributes = {
            "title": "not so urgent",
        }
        tag_2 = TestViewSetBase.create(self, data=tag_2_attributes)
        response = self.list()
        expected_response = [
            self.expected_details({"id": tag["id"]}, self.tag_attributes),
            self.expected_details({"id": tag_2["id"]}, tag_2_attributes),
        ]
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json() == expected_response

    def test_retrieve(self):
        tag = TestViewSetBase.create(self, data=self.tag_attributes)
        response = self.retrieve(key=tag["id"])
        assert response.json() == self.expected_details(
            {"id": tag["id"]}, self.tag_attributes
        )

    def test_update(self):
        tag = TestViewSetBase.create(self, data=self.tag_attributes)
        self.tag_attributes["title"] = "To kill a mockingbird"
        response = self.update(
            key=tag["id"],
            data=self.tag_attributes,
        )
        assert response.status_code == HTTPStatus.OK, response.content
        assert response.json()["title"] == "To kill a mockingbird"

    def test_delete(self):
        tag = TestViewSetBase.create(self, data=self.tag_attributes)
        response = self.delete(key=tag["id"])
        response_list = self.list()
        assert response.status_code == HTTPStatus.NO_CONTENT, response.content
        assert response_list.json() == []

    def test_unauthenticated_request(self):
        response = self.unauthenticated_request()
        assert response.status_code == HTTPStatus.FORBIDDEN

    def test_filter(self):
        tag = TestViewSetBase.create(self, data=self.tag_attributes)
        tag_2_attributes = {
            "title": "not so urgent",
        }
        tag_2 = TestViewSetBase.create(self, data=tag_2_attributes)
        filter_field = "title"
        filter_value = "urgent"
        tags = self.list().json()
        expected_tags: list = []
        for tag in tags:
            if filter_value in tag[filter_field]:
                expected_tags.append(tag)
                break
        response = self.filter(filter_field=filter_field, filter_value=filter_value)
        assert response == expected_tags
