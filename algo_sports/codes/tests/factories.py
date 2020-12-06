from factory import Faker, Sequence, fuzzy
from factory.declarations import SubFactory
from factory.django import DjangoModelFactory

from algo_sports.codes.models import JudgementCode, ProgrammingLanguage, UserCode
from algo_sports.games.tests.factories import GameInfoFactory
from algo_sports.users.tests.factories import UserFactory

fake_word = Faker("word")


class ProgrammingLanguageFactory(DjangoModelFactory):
    name = Sequence(lambda x: f"{fake_word.generate()} {x}")

    class Meta:
        model = ProgrammingLanguage


class UserCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)

    programming_language = SubFactory(ProgrammingLanguageFactory)
    code = Faker("sentence")
    is_active = fuzzy.FuzzyInteger(0, 1)

    class Meta:
        model = UserCode


class JudgementCodeFactory(DjangoModelFactory):
    user_id = SubFactory(UserFactory)
    gameinfo_id = SubFactory(GameInfoFactory)

    programming_language = SubFactory(ProgrammingLanguageFactory)
    code = Faker("sentence")

    class Meta:
        model = JudgementCode
