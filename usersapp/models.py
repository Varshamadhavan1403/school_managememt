from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model with additional methods
    to create office staff and superusers.
    """

    def create_user(self, username, email, password=None, role="staff", **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # Validate the role
        if role not in dict(User.ROLES):
            raise ValueError(f"Invalid role: {role}")

        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_office_staff(self, username, email, password=None, **extra_fields):
        """
        Create and return an office staff user.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(username, email, password, role="staff", **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and return a superuser with admin privileges.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, role="admin", **extra_fields)


class User(AbstractUser):
    """
    Custom User model that includes a role field.
    """

    ROLES = (
        ("admin", "Admin"),
        ("staff", "Office Staff"),
        ("librarian", "Librarian"),
    )
    role = models.CharField(max_length=50, choices=ROLES, default="staff")

    objects = UserManager()  # Custom user manager

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
