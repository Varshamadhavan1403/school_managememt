from rest_framework import serializers
from datetime import date

from .models import FeesHistory


class FeeHistorySerializers(serializers.ModelSerializer):
    remarks = serializers.CharField(
        required=True, allow_blank=False
    )  # Remarks is required

    class Meta:
        model = FeesHistory
        fields = ["id", "student", "fee_type", "amount", "payment_date", "remarks"]
        read_only_fields = ["id"]  # Prevent modification of ID

    def validate_amount(self, value):
        """
        Validate the amount to ensure it is greater than 0.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_payment_date(self, value):
        """
        Validate the payment_date to ensure it is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError("Payment date cannot be in the future.")
        return value

    def validate(self, data):
        """
        Object-level validation to prevent duplicate records.
        """
        student = data.get("student")
        fee_type = data.get("fee_type")
        payment_date = data.get("payment_date")

        # Ensure required fields exist
        if not student or not fee_type or not payment_date:
            raise serializers.ValidationError(
                "Student, fee_type, and payment_date are required."
            )

        # Exclude the current instance from duplicate check during update
        request_instance_id = self.instance.id if self.instance else None
        duplicate_exists = (
            FeesHistory.objects.filter(
                student=student, fee_type=fee_type, payment_date=payment_date
            )
            .exclude(id=request_instance_id)
            .exists()
        )

        if duplicate_exists:
            raise serializers.ValidationError(
                {
                    "non_field_errors": "This fee type has already been recorded for the student on this date."
                }
            )

        return data
