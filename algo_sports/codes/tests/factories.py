from factory import Faker, Sequence
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from algo_sports.codes.models import JudgementCode, ProgrammingLanguage, UserCode
from algo_sports.games.tests.factories import GameInfoFactory
from algo_sports.users.tests.factories import UserFactory


class ProgrammingLanguageFactory(DjangoModelFactory):
    name = Sequence(lambda n: "PL %d" % n)

    class Meta:
        model = ProgrammingLanguage


class UserCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)

    programming_language = SubFactory(ProgrammingLanguageFactory)
    code = Faker("sentence")

    class Meta:
        model = UserCode


class JudgementCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)
    gameinfo_id = SubFactory(GameInfoFactory)

    programming_language = SubFactory(ProgrammingLanguageFactory)
    code = Faker("sentence")

    class Meta:
        model = JudgementCode
