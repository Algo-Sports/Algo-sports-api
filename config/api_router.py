from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from algo_sports.codes.views import JudgementCodeViewSet, UserCodeViewSet
from algo_sports.games.views import GameInfoViewSet, GameRoomViewSet
from algo_sports.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("games/info", GameInfoViewSet)
router.register("games/room", GameRoomViewSet)
router.register("codes/user", UserCodeViewSet)
router.register("codes/judegement", JudgementCodeViewSet)


app_name = "api"
urlpatterns = router.urls
