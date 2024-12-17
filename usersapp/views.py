from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import (
    AddOfficeStaffSerializers,
    AdminTokenObtainPairSerializers,
    AddLibrarianSerializers,
    StaffTokenObtainPairSerializers,
    LibrarianTokenObtainPairSerializers,
    EditAccountsSerializers,
)
from .permissions import IsAdmin


# Admin Token Obtain View
class AdminTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView for Admin users to obtain JWT tokens.
    This view uses a custom serializer to include the admin role in the JWT token.
    """

    serializer_class = AdminTokenObtainPairSerializers


# Create Office Staff View
class CreateOfficeStaffView(APIView):
    """
    View to create a new office staff account.
    Accessible only by authenticated admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        """
        Handles POST requests to create a new office staff member.
        If the serializer is valid, the office staff account is created and a success message is returned.
        """
        serializer = AddOfficeStaffSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Office staff account created successfully",
                             "data" : serializer.data
                             })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Edit Office Staff View
class EditOfficeStaffView(APIView):
    """
    View to update an existing office staff account.
    Accessible only by authenticated admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        """
        Retrieve the office staff member by their primary key (pk).
        Returns None if the office staff is not found.
        """
        try:
            return User.objects.get(pk=pk, role="staff")
        except User.DoesNotExist:
            return None

    def put(self, request, pk):
        """
        Handles PUT requests to update the office staff account.
        Returns success or failure based on the validation of the serializer.
        """
        office_staff = self.get_object(pk)
        if not office_staff:
            return Response(
                {"details": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EditAccountsSerializers(
            office_staff, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Office staff updated successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Office Staff View
class DeleteOfficeStaffView(APIView):
    """
    View to delete an office staff account.
    Accessible only by authenticated admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        """
        Retrieve the office staff member by their primary key (pk).
        Returns None if the office staff is not found.
        """
        try:
            return User.objects.get(pk=pk, role="staff")
        except User.DoesNotExist:
            return None

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove an office staff account.
        Returns success or failure based on whether the staff exists.
        """
        office_staff = self.get_object(pk)
        if not office_staff:
            return Response(
                {"details": "Office staff not found."}, status=status.HTTP_404_NOT_FOUND
            )
        office_staff.delete()
        return Response(
            {"message": "Office staff deleted successfully"}, status=status.HTTP_200_OK
        )


# Staff Token Obtain View
class StaffTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView for Staff users to obtain JWT tokens.
    This view uses a custom serializer to include the staff role in the JWT token.
    """

    serializer_class = StaffTokenObtainPairSerializers


# Create Librarian View
class CreateLibrarianView(APIView):
    """
    View to create a new librarian account.
    Accessible only by authenticated admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        """
        Handles POST requests to create a new librarian.
        If the serializer is valid, the librarian account is created and a success message is returned.
        """
        serializer = AddLibrarianSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Librarian account created successfully",
                            "data" : serializer.data
                            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Edit Librarian View
class EditLibrarianView(APIView):
    """
    View to update an existing librarian account.
    Accessible only by authenticated admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        """
        Retrieve the librarian by their primary key (pk).
        Returns None if the librarian is not found.
        """
        try:
            return User.objects.get(pk=pk, role="librarian")
        except User.DoesNotExist:
            return None

    def put(self, request, pk):
        """
        Handles PUT requests to update the librarian account.
        Returns success or failure based on the validation of the serializer.
        """
        librarian_staff = self.get_object(pk)
        if not librarian_staff:
            return Response(
                {"details": "Librarian not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = EditAccountsSerializers(
            librarian_staff, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Librarian updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Librarian View
class DeleteLibrarianView(APIView):
    """
    View to delete a librarian account.
    Accessible only by authenticated admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        """
        Retrieve the librarian by their primary key (pk).
        Returns None if the librarian is not found.
        """
        try:
            return User.objects.get(pk=pk, role="librarian")
        except User.DoesNotExist:
            return None

    def delete(self, request, pk):
        """
        Handles DELETE requests to remove a librarian account.
        Returns success or failure based on whether the librarian exists.
        """
        librarian_staff = self.get_object(pk)
        if not librarian_staff:
            return Response(
                {"details": "Librarian not found."}, status=status.HTTP_404_NOT_FOUND
            )
        librarian_staff.delete()
        return Response(
            {"message": "Librarian deleted successfully"}, status=status.HTTP_200_OK
        )


# Librarian Token Obtain View
class LibrarianTokenObtainPairView(TokenObtainPairView):
    """
    Custom TokenObtainPairView for Librarian users to obtain JWT tokens.
    This view uses a custom serializer to include the librarian role in the JWT token.
    """

    serializer_class = LibrarianTokenObtainPairSerializers
