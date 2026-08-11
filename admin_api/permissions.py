from rest_framework import permissions


def get_user_role(user):
    try:
        return user.userrole.role
    except Exception:
        return 'admin' if user.is_superuser else 'cashier'


class IsAdminOrCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.userrole.role in ['admin', 'cashier']
        except Exception:
            return request.user.is_staff


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.userrole.role == 'admin'
        except Exception:
            return request.user.is_staff


class IsCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        try:
            return request.user.userrole.role in ['admin', 'cashier']
        except Exception:
            return request.user.is_staff
