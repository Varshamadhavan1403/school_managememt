from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import LibraryHistorySerializer
from .models import LibraryHistory
from students.models import Student
from students.serializers import StudentSerializers
from usersapp.permissions import IsAdmin, IsOfficeStaff, IsLibrarian


class LibraryHistoryView(generics.ListCreateAPIView):
    """
    View to list and create library history records.
    Accessible only to Admin.
    """

    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class LibraryHistoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a library history record.
    Accessible only to Admin.
    """

    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def destroy(self, request, *args, **kwargs):
        """
        Custom destroy method to include a success message with additional context.
        """
        library_record = self.get_object()
        book_name = library_record.book_name
        student_name = library_record.student.name
        borrow_date = library_record.borrow_date

        # Call the superclass method to delete the record
        super().destroy(request, *args, **kwargs)

        # Return a custom success message
        return Response(
            {
                "message": (
                    f"Library history for book '{book_name}' borrowed by "
                    f"'{student_name}' on {borrow_date} has been deleted successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


class LibrarianStudentListView(generics.ListAPIView):
    """
    View for librarians and office staff to list all students.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializers
    permission_classes = [IsAuthenticated, IsLibrarian | IsOfficeStaff]


class LibrarianLibraryHistoryListView(generics.ListAPIView):
    """
    View for librarians and office staff to list all library history records.
    """

    queryset = LibraryHistory.objects.all()
    serializer_class = LibraryHistorySerializer
    permission_classes = [IsAuthenticated, IsLibrarian | IsOfficeStaff]
