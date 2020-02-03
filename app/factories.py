from django.contrib.auth import get_user_model

import factory
from factory import Faker, fuzzy

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    email = Faker("email")
    username = fuzzy.FuzzyText(length=15)
    password = factory.PostGenerationMethodCall('set_password', '1234asdf')

    class Meta:
        model = User
