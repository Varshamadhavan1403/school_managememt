from rest_framework.permissions import BasePermission


# Permission class to check if the user is an admin
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has an 'admin' role
        return request.user.is_authenticated and request.user.role == "admin"


# Permission class to check if the user is a staff member (office staff)
class IsOfficeStaff(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has a 'staff' role
        return request.user.is_authenticated and request.user.role == "staff"


# Permission class to check if the user is a librarian
class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        # Check if the user is authenticated and has a 'librarian' role
        return request.user.is_authenticated and request.user.role == "librarian"
