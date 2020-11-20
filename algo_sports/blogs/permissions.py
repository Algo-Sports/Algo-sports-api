from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsCommentNotDeleted(BasePermission):
    """
    삭제된 Comment에는 수정, 삭제 불가
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return not obj.deleted
