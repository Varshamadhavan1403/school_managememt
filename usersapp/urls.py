from django.urls import path
from .views import (
    CreateOfficeStaffView,
    AdminTokenObtainPairView,
    CreateLibrarianView,
    StaffTokenObtainPairView,
    LibrarianTokenObtainPairView,
    EditOfficeStaffView,
    DeleteOfficeStaffView,
    EditLibrarianView,
    DeleteLibrarianView,
)

urlpatterns = [
    path(
        "create_office_staff/",
        CreateOfficeStaffView.as_view(),
        name="create-office-staff",
    ),
    path("admin_login/", AdminTokenObtainPairView.as_view(), name="admin_login"),
    path("create_librarian/", CreateLibrarianView.as_view(), name="create_librarian"),
    path("staff_login/", StaffTokenObtainPairView.as_view(), name="staff-login"),
    path(
        "librarian_login/",
        LibrarianTokenObtainPairView.as_view(),
        name="librarian-login",
    ),
    path(
        "update_office_staff/<int:pk>/",
        EditOfficeStaffView.as_view(),
        name="update_staff",
    ),
    path(
        "delete_office_staff/<int:pk>/",
        DeleteOfficeStaffView.as_view(),
        name="delete-office-staff",
    ),
    path(
        "update_librarian/<int:pk>/",
        EditLibrarianView.as_view(),
        name="update-librarian",
    ),
    path(
        "delete_librarian/<int:pk>/",
        DeleteLibrarianView.as_view(),
        name="delete-librarian",
    ),
]
