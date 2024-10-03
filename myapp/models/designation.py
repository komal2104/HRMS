from django.db import models

class Designation(models.Model):
    """
    Model representing a designation or job title within the organization.

    Attributes:
        name (CharField): The name of the designation.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        """
        Returns a string representation of the designation.

        This method returns the name of the designation.
        """
        return self.name
