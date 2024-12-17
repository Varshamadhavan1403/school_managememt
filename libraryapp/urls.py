from django.urls import path
from .views import (
    LibraryHistoryView,
    LibraryHistoryDetailView,
    LibrarianLibraryHistoryListView,
)

urlpatterns = [
    path(
        "create_library_history/",
        LibraryHistoryView.as_view(),
        name="create-library-history",
    ),
    path(
        "library_details/<int:pk>/",
        LibraryHistoryDetailView.as_view(),
        name="library-details",
    ),
    path(
        "view_library_history/",
        LibrarianLibraryHistoryListView.as_view(),
        name="view-library-history",
    ),
]
