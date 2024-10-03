from django.db import models
from .user import User

class Attendance(models.Model):
    """
    Model representing attendance records for users.

    Attributes:
        user (ForeignKey): The user associated with this attendance record.
        date (DateField): The date for which the attendance is recorded.
        marked (BooleanField): A flag indicating whether the user was present (True) or absent (False).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    marked = models.BooleanField(default=True)

    def __str__(self):
        """
        Returns a string representation of the attendance record.

        The format includes the username, date, and attendance status (Present/Absent).
        """
        return f"{self.user.username} - {self.date} - {'Present' if self.marked else 'Absent'}"
