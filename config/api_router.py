from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from algo_sports.blogs.views import BlogViewSet, CommentViewSet, PostViewSet
from algo_sports.codes.views import JudgementCodeViewSet, UserCodeViewSet
from algo_sports.games.views import GameInfoViewSet, GameRoomViewSet
from algo_sports.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# users
router.register("users", UserViewSet)

# games app api viewsets
router.register("games/info", GameInfoViewSet)
router.register("games/room", GameRoomViewSet)

# codes app api viewsets
router.register("codes/user", UserCodeViewSet)
router.register("codes/judegement", JudgementCodeViewSet)

# blogs app api viewsets
router.register("blogs", BlogViewSet)
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)


app_name = "api"
urlpatterns = router.urls
