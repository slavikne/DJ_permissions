from rest_framework.permissions import BasePermission



class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsAdminOrOwner (BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user or request.user.is_staff:
            return True
        else:
            return False


