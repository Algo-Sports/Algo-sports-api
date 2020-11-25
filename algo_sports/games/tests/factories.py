from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from algo_sports.games.choices import GameStatus, GameType
from algo_sports.games.models import GameInfo, GameRoom


class GameInfoFactory(DjangoModelFactory):
    title = Faker("sentence")
    version = Faker("word")
    description = Faker("sentence")

    min_users = FuzzyInteger(2, 4)
    max_users = FuzzyInteger(5, 10)

    extra_info = {
        "game_setting1": {
            "customize": True,
            "varient": 1000,
        },
    }

    class Meta:
        model = GameInfo


class GameRoomFactory(DjangoModelFactory):
    gameinfo_id = SubFactory(GameInfoFactory)
    type = FuzzyChoice(GameType.values)
    status = FuzzyChoice(GameStatus.values)
    setting = {
        "game_setting1": {
            "varient": 300,
        },
    }

    class Meta:
        model = GameRoom
