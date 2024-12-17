from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from students.models import Student


class FeesHistory(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="fees_history"
    )
    fee_type = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()
    remarks = models.TextField(null=True, blank=True)

    def clean(self):
        """
        Validates the model fields.
        """
        # Ensure the amount is positive
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

        # Ensure the payment_date is not in the future
        if self.payment_date > date.today():
            raise ValidationError("Payment date cannot be in the future.")

        # Prevent duplicate records for the same student, fee_type, and payment_date
        if (
            FeesHistory.objects.filter(
                student=self.student,
                fee_type=self.fee_type,
                payment_date=self.payment_date,
            )
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                "This fee type already exists for the student on this date."
            )

    def save(self, *args, **kwargs):
        """
        Overrides the save method to include validation.
        """
        self.clean()  # Call the clean method before saving
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the model.
        """
        return f"{self.student.name} - {self.fee_type}: {self.amount}"
