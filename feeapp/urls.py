from django.urls import path
from .views import FeeHistoryView, FeesHistorydetailView

urlpatterns = [
    path("create_fees/", FeeHistoryView.as_view(), name="create-fees"),
    path(
        "fees_details/<int:pk>/", FeesHistorydetailView.as_view(), name="fees-details"
    ),
]
