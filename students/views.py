from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .models import Student
from .serializers import StudentSerializers
from usersapp.permissions import IsAdmin, IsOfficeStaff
from rest_framework.response import Response


class CreateStudentListView(generics.CreateAPIView):
    """
    View to create a new student record. Accessible only by authenticated Admin users.
    """

    # Define the queryset to be used in the view (all student records).
    queryset = Student.objects.all()

    # Define the serializer class for serializing student data.
    serializer_class = StudentSerializers

    # Define the permission classes, ensuring only authenticated Admin users can access this view.
    permission_classes = [IsAuthenticated, IsAdmin]


# View to retrieve, update, or delete a student record.
# This view is accessible to both Admins and Office Staff.
class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a student record.
    Accessible only by authenticated Admin and Office Staff users.
    """

    # Define the queryset to be used in the view (all student records).
    queryset = Student.objects.all()

    # Define the serializer class for serializing student data.
    serializer_class = StudentSerializers

    # Define the permission classes, allowing Admin and Office Staff access.
    permission_classes = [IsAuthenticated, IsAdmin | IsOfficeStaff]

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to handle the deletion of a student record.
        It returns a custom success message after deletion.
        """
        # Retrieve the student instance to be deleted.
        student = self.get_object()

        # Store the student name for use in the response message.
        student_name = student.name

        # Call the superclass destroy method to delete the student record.
        super().destroy(request, *args, **kwargs)

        # Return a custom success message indicating that the student has been deleted.
        return Response(
            {"message": f"Student '{student_name}' has been deleted successfully."},
            status=status.HTTP_200_OK,
        )
