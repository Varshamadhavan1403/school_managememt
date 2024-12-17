from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import FeesHistory
from .serializers import FeeHistorySerializers
from usersapp.permissions import IsAdmin, IsOfficeStaff


class FeeHistoryView(generics.ListCreateAPIView):
    """
    View to list and create fee history records.
    Accessible only to Admin and Office Staff.
    """

    queryset = FeesHistory.objects.all()
    serializer_class = FeeHistorySerializers
    permission_classes = [IsAuthenticated, IsAdmin | IsOfficeStaff]


class FeesHistorydetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a fee history record.
    """

    queryset = FeesHistory.objects.all()
    serializer_class = FeeHistorySerializers
    permission_classes = [IsAuthenticated, IsAdmin | IsOfficeStaff]

    def destroy(self, request, *args, **kwargs):
        # Retrieve the fee record instance
        fee_record = self.get_object()

        # Get student and fee type details
        student_name = fee_record.student.name
        fee_type = fee_record.fee_type

        # Call the superclass destroy method to delete the record
        super().destroy(request, *args, **kwargs)

        # Return a custom success message
        return Response(
            {
                "message": f"Fees record for student '{student_name}' ({fee_type}) has been deleted successfully."
            },
            status=status.HTTP_200_OK,
        )
