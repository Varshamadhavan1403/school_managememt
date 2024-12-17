from django.urls import path
from .views import CreateStudentListView, StudentDetailView

urlpatterns = [
    path("create_student/", CreateStudentListView.as_view(), name="create-student"),
    path(
        "student_detail/<int:pk>/", StudentDetailView.as_view(), name="student-detail"
    ),
]
