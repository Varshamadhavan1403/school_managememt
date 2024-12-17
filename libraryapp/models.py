from datetime import date
from django.db import models
from django.core.exceptions import ValidationError
from students.models import Student


class LibraryHistory(models.Model):
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="library_history"
    )
    book_name = models.CharField(max_length=255)
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=[("borrowed", "Borrowed"), ("returned", "Returned")],
        default="borrowed",
    )

    def __str__(self):
        return f"{self.book_name} - {self.student.name}"

    def clean(self):
        """
        Validates the model fields.
        """
        # Borrow date must not be in the future
        if self.borrow_date > date.today():
            raise ValidationError("Borrow date cannot be in the future.")

        # Return date must be after borrow date
        if self.return_date and self.return_date < self.borrow_date:
            raise ValidationError("Return date cannot be earlier than borrow date.")

        # Return date is required if status is 'returned'
        if self.status == "returned" and not self.return_date:
            raise ValidationError(
                "Return date must be provided if status is 'returned'."
            )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(status="borrowed") | models.Q(return_date__isnull=False),
                name="return_date_required_for_returned_status",
            )
        ]
