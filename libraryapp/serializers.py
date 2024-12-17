from rest_framework import serializers
from datetime import date
from .models import LibraryHistory


class LibraryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryHistory
        fields = ["id", "student", "book_name", "borrow_date", "return_date", "status"]
        # Prevent status from being explicitly set
        read_only_fields = ["status"]

    def validate(self, data):
        """
        Object-level validation for borrow_date and return_date.
        """
        borrow_date = data.get("borrow_date")
        return_date = data.get("return_date")

        # Ensure borrow_date is not in the future
        if borrow_date and borrow_date > date.today():
            raise serializers.ValidationError(
                {"borrow_date": "Borrow date cannot be in the future."}
            )

        # Ensure return_date is after borrow_date
        if return_date and borrow_date and return_date < borrow_date:
            raise serializers.ValidationError(
                {"return_date": "Return date cannot be earlier than borrow date."}
            )

        # Ensure return_date is provided if status is 'returned'
        status = data.get("status", "borrowed")
        if status == "returned" and not return_date:
            raise serializers.ValidationError(
                {"return_date": "Return date must be provided if status is 'returned'."}
            )

        return data

    def _update_status(self, validated_data):
        """
        Helper method to set status to 'returned' if return_date is provided.
        """
        if validated_data.get("return_date"):
            validated_data["status"] = "returned"
        return validated_data

    def create(self, validated_data):
        """
        Automatically set the status to 'returned' if return_date is provided during creation.
        """
        validated_data = self._update_status(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Automatically update the status to 'returned' if return_date is provided during update.
        """
        validated_data = self._update_status(validated_data)
        return super().update(instance, validated_data)
