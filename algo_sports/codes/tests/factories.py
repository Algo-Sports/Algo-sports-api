from factory import Faker, Sequence, fuzzy
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from algo_sports.codes.models import JudgementCode, ProgrammingLanguage, UserCode
from algo_sports.games.tests.factories import GameRoomFactory, GameVersionFactory
from algo_sports.users.tests.factories import UserFactory

fake_word = Faker("word")


class ProgrammingLanguageFactory(DjangoModelFactory):
    name = Sequence(lambda x: f"{fake_word.generate()} {x}")

    class Meta:
        model = ProgrammingLanguage


class UserCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)
    gamerooms = SubFactory(GameRoomFactory)

    programming_language = SubFactory(ProgrammingLanguageFactory)
    code = Faker("sentence")
    is_active = fuzzy.FuzzyInteger(0, 1)

    class Meta:
        model = UserCode


class JudgementCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)
    gameversion_id = SubFactory(GameVersionFactory)

    programming_language = SubFactory(ProgrammingLanguageFactory)
    code = Faker("sentence")

    class Meta:
        model = JudgementCode
