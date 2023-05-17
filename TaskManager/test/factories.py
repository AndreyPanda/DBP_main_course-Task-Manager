import random
import factory
from factory import Faker
from django.core.files.uploadedfile import SimpleUploadedFile
from faker.providers import BaseProvider
from main.models import User, Task
from django.contrib.auth.hashers import make_password


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )


Faker.add_provider(ImageFileProvider)


class UserFactory(factory.Factory):
    email = Faker("email")
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    username = Faker("user_name")
    password = make_password("password")
    role = random.choice(User.Roles.choices)[0]
    avatar_picture = Faker("image_file", fmt="jpeg")

    class Meta:
        model = dict


class TaskFactory(factory.Factory):
    title = Faker("sentence")
    description = Faker("sentence")
    state = Task.States.NEW_TASK
    priority = Task.Priority.MEDIUM
    executor = Faker("user_name")

    class Meta:
        model = dict


class LargeAvatarUserFactory(UserFactory):
    avatar_picture = SimpleUploadedFile("large.jpg", b"x" * 2 * 1024 * 1024)
