from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUser(BasePermission):
    """
    superuser는 모든 권한을 가진다.
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsAdminUser(BasePermission):
    """
    Admin users만 접근 가능
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        print("access : ", request.user.is_admin)
        return bool(request.user and request.user.is_admin)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        print("object : ", request.user.is_admin)
        return bool(request.user and request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    """
    Admin users만 Post 가능하도록
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_admin)


class IsOwnerOrReadOnly(BasePermission):
    """
    해당 객체를 생성한 user만 권한을 부여
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
