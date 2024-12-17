from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

from .models import User


class AdminTokenObtainPairSerializers(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer to include the user's role in the JWT token.
    Also restricts access to admins only.
    """

    @classmethod
    def get_token(cls, user):
        # Get the base token and add a custom claim for the role
        token = super().get_token(user)

        # Add the role of the user as a custom claim in the token
        token["role"] = user.role
        return token

    def validate(self, attrs):
        """
        Validate the credentials and check if the user has the 'admin' role.
        If not, raise an AuthenticationFailed error.
        """
        data = super().validate(attrs)
        print(f"User Role: {self.user.role}")

        # Restrict access to users with the 'admin' role
        if self.user.role != "admin":
            raise AuthenticationFailed(
                "You do not have permission to access this resource"
            )
        # Include the role in the response data
        data["role"] = self.user.role
        return data


class AddOfficeStaffSerializers(serializers.ModelSerializer):
    """
    Serializer to create a new office staff user.
    The user is assigned a role of 'staff' by default.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}  # Ensure password is not included in responses
        }

    def validate_username(self, value):
        """
        Validate that the username is unique and contains only alphanumeric characters.
        """
        if not value.isalnum():
            raise serializers.ValidationError(
                "The username should contain only letters and numbers."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_email(self, value):
        """
        Validate the email format and check if it already exists.
        """
        try:
            validate_email(value)  # Check for a valid email format
        except serializers.ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )
        return value

    def validate_password(self, value):
        """
        Validate the password using Django's built-in password validators.
        """
        validate_password(value)  # Check password strength and complexity
        return value

    def validate(self, attrs):
        """
        Perform additional object-level validation if needed.
        """
        if attrs["username"].lower() == attrs["email"].split("@")[0].lower():
            raise serializers.ValidationError(
                "Username and email local part should not be the same."
            )
        return attrs

    def create(self, validated_data):
        """
        Create a new office staff user, assigning the default role as 'staff'.
        """
        # Create the user with the provided data and assign the 'staff' role
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        # Set the user's role and mark them as active and staff
        user.role = "staff"
        user.is_active = True
        user.is_staff = True
        user.save()
        return user



class EditAccountsSerializers(serializers.ModelSerializer):
    """
    Serializer to update user details, including username and password,
    while preventing updates to the email field.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},  # Password is optional for update
        }

    def update(self, instance, validated_data):
        """
        Update user details, preventing email updates and hashing the password if provided.
        """
        # Prevent email from being updated by removing it from validated_data
        if "email" in validated_data:
            validated_data.pop("email")

        # Update username if provided
        instance.username = validated_data.get("username", instance.username)

        # If a new password is provided, hash it and update the password
        if "password" in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()
        return instance

class StaffTokenObtainPairSerializers(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer for staff users.
    Ensures only 'staff' users can log in and adds role to token.
    """

    def validate(self, attrs):
        """
        Validate credentials and check if the user has the 'staff' role.
        If not, raise an AuthenticationFailed error.
        """
        data = super().validate(attrs)

        # Ensure the user's account is active
        if not self.user.is_active:
            raise AuthenticationFailed("This account is inactive.")

        # Restrict access to users with the 'staff' role
        if self.user.role != "staff":
            raise AuthenticationFailed(
                "You do not have permission to access this resource."
            )

        # Add the role of the user to the response data
        data["role"] = self.user.role
        return data


class AddLibrarianSerializers(serializers.ModelSerializer):
    """
    Serializer to create a new librarian user.
    The user is assigned a role of 'librarian' by default.
    """

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }  # Ensure password is not included in responses
    
    def validate_username(self, value):
        """
        Validate that the username is unique and contains only alphanumeric characters.
        """
        if not value.isalnum():
            raise serializers.ValidationError(
                "The username should contain only letters and numbers."
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    def validate_email(self, value):
        """
        Validate the email format and check if it already exists.
        """
        try:
            validate_email(value)  # Check for a valid email format
        except serializers.ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email address already exists."
            )
        return value

    def validate_password(self, value):
        """
        Validate the password using Django's built-in password validators.
        """
        validate_password(value)  # Check password strength and complexity
        return value

    def validate(self, attrs):
        """
        Perform additional object-level validation if needed.
        """
        if attrs["username"].lower() == attrs["email"].split("@")[0].lower():
            raise serializers.ValidationError(
                "Username and email local part should not be the same."
            )
        return attrs


    def create(self, validated_data):
        """
        Create a new librarian user, assigning the default role as 'librarian'.
        """
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.role = "librarian"
        user.save()
        return user


class LibrarianTokenObtainPairSerializers(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer for librarian users.
    Ensures only 'librarian' users can log in and adds role to token.
    """

    def validate(self, attrs):
        """
        Validate credentials and check if the user has the 'librarian' role.
        If not, raise an AuthenticationFailed error.
        """
        data = super().validate(attrs)

        # Ensure the user's account is active
        if not self.user.is_active:
            raise AuthenticationFailed("This account is inactive.")

        # Restrict access to users with the 'librarian' role
        if self.user.role != "librarian":
            raise AuthenticationFailed(
                "You do not have permission to access this resource."
            )

        # Add the role of the user to the response data
        data["role"] = self.user.role
        return data
