from factory.declarations import SubFactory
from factory.django import DjangoModelFactory
from factory.faker import Faker

from algo_sports.games.models import GameInfo, GameRoom


class GameInfoFactory(DjangoModelFactory):
    title = Faker("title")
    version = Faker("version")
    description = Faker("description")

    min_users = Faker("min_users")
    max_users = Faker("max_users")

    extra_info = Faker("extra_info")

    class Meta:
        model = GameInfo


class GameRoomFactory(DjangoModelFactory):
    gameinfo_id = SubFactory(GameInfoFactory)
    status = Faker("status")

    class Meta:
        model = GameRoom
