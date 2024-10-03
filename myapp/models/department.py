from django.db import models

class Department(models.Model):
    """
    Model representing a department within the organization.

    Attributes:
        name (CharField): The name of the department.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the department.

        This method returns the name of the department.
        """
        return self.name
