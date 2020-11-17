from django.contrib.auth import get_user_model
from django.db import models

from algo_sports.utils.choices import PermissionChoices

User = get_user_model()


class Blog(models.Model):
    category = models.CharField("Blog cateogry", max_length=2)
    permission = models.CharField(
        "Blog permission",
        max_length=2,
        choices=PermissionChoices.choices,
        default=PermissionChoices.ALL,
    )
    description = models.TextField("Blog description", max_length=2)

    class Meta:
        ordering = ["category"]

    def __str__(self) -> str:
        return f"{self.category} ({self.permission})"

    @classmethod
    def permission_choices(cls):
        """ permission choices """
        return PermissionChoices.choices

    @property
    def gameinfo(self):
        return self.gameinfo_id


class Post(models.Model):
    title = models.TextField("Post title")

    user_id = models.ForeignKey(
        User,
        verbose_name="Post author",
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )
    blog_id = models.ForeignKey(
        Blog,
        verbose_name="Post of comment",
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )

    content = models.TextField("Post content")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return self.title

    @property
    def user(self):
        return self.user_id

    @property
    def blog(self):
        return self.blog_id

    def get_comments(self):
        return self.comments.all()


class Comment(models.Model):
    post_id = models.ForeignKey(
        Post,
        verbose_name="Comment of post",
        on_delete=models.PROTECT,
        related_name="comments",
    )
    user_id = models.ForeignKey(
        User,
        verbose_name="Comment author",
        null=True,
        on_delete=models.SET_NULL,
        related_name="comments",
    )
    parent_id = models.ForeignKey(
        "Comment",
        null=True,
        blank=True,
        verbose_name="Parent Comment",
        on_delete=models.PROTECT,
        related_name="childs",
    )

    deleted = models.BooleanField("Is Comment deleted?", default=False)
    content = models.CharField("Comment content", max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self) -> str:
        return f"Comment({self.id})"

    @property
    def post(self):
        return self.post_id

    @property
    def user(self):
        return self.user_id

    @property
    def parent(self):
        return self.parent_id

    def fake_delete(self):
        """ Fake delete """
        self.deleted = True

    def get_childs(self):
        """ Get child comments """
        return self.childs.all()
