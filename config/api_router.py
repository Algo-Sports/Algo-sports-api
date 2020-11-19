from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from algo_sports.blogs.views import BlogViewSet, CommentViewSet, PostViewSet
from algo_sports.users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("blogs", BlogViewSet)
router.register("posts", PostViewSet)
router.register("comments", CommentViewSet)


app_name = "api"
urlpatterns = router.urls
