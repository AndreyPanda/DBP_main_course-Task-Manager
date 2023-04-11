from factory import Faker
from main.models import User
from factory.django import DjangoModelFactory
from factory import PostGenerationMethodCall


class UserFactory(DjangoModelFactory):
    username = Faker("user_name")
    password = PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
