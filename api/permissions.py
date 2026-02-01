from rest_framework.permissions import BasePermission


class IsOwnerOrManager(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # obj is expected to be a Car instance
        user = request.user
        if user.groups.filter(name="Managers").exists():
            return True
        return getattr(obj, "owner_id", None) == user.id