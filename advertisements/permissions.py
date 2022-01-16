from rest_framework.permissions import BasePermission
from django.contrib.auth.models import User


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class IsAdminOrOwner (BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.creator == request.user or User.objects.filter(
                username=request.user).values('is_staff')[0].get('is_staff'):
            return True
        else:
            return False

