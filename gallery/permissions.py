from rest_framework import permissions


class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_admin or request.user.is_staff


class IsOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_anonymous and (request.user.is_admin
                                                  or request.user.is_staff)
