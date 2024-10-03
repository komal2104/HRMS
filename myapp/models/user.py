from django.db import models
from .designation import Designation
from .department import Department

class User(models.Model):
    """
    Model representing a user in the organization.

    Attributes:
        name (CharField): The name of the user.
        email (EmailField): The user's email address, which must be unique.
        designation (ForeignKey): The designation associated with the user.
        department (ForeignKey): The department associated with the user.
        date_of_joining (DateField): The date the user joined the organization.
        is_active (BooleanField): A flag indicating whether the user is currently active.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date_of_joining = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns a string representation of the user.

        This method returns the name of the user.
        """
        return self.name
