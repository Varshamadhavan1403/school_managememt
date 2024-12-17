from django.db import models

"""
The Student model represents a student entity in the database.
It includes fields like name, age, grade, and created_at to store relevant information.
"""


class Student(models.Model):
    # The 'name' field stores the student's full name with a maximum length of 100 characters.
    name = models.CharField(max_length=100)

    # The 'age' field stores the student's age as an integer.
    age = models.IntegerField()

    # The 'grade' field stores the student's grade as a string with a maximum length of 20 characters.
    grade = models.CharField(max_length=20)

    # The 'created_at' field automatically stores the date and time when the student record is created.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        The __str__ method is used to return a human-readable representation of the object.
        In this case, it returns the student's name.
        """
        return self.name
