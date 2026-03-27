from rest_framework.permissions import BasePermission


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'CUSTOMER'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'CUSTOMER'


class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'SUPPORT'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'SUPPORT'


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'ADMIN'

    def has_object_permission(self, request, view, obj):
        return request.user.role == 'ADMIN'
