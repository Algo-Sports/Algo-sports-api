from factory import Faker
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from algo_sports.codes.models import JudgementCode, UserCode
from algo_sports.games.tests.factories import GameInfoFactory
from algo_sports.users.tests.factories import UserFactory


class UserCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)

    programming_language = Faker("programming_language")
    code = Faker("code")

    class Meta:
        model = UserCode


class JudgementCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)
    gameinfo_id = SubFactory(GameInfoFactory)

    programming_language = Faker("programming_language")
    code = Faker("code")

    class Meta:
        model = JudgementCode
