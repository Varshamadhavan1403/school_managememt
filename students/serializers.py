from rest_framework import serializers
from .models import Student

"""
The StudentSerializers class is a ModelSerializer that converts
Student model instances into JSON format and vice versa.
"""


class StudentSerializers(serializers.ModelSerializer):
    # Meta class defines the model and fields to be serialized.
    class Meta:
        model = Student  # Specify the model to serialize
        fields = [
            "id",
            "name",
            "age",
            "grade",
        ]  # Fields to include in the serialized output
