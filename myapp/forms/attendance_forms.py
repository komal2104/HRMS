from django import forms
from ..models.user import User
from ..models.attendance import Attendance

class AttendanceForm(forms.ModelForm):
    """
    Form for creating or updating attendance records.

    Meta class specifies the model and fields to include in the form.
    """
    class Meta:
        model = Attendance
        fields = ['user', 'date']

    def __init__(self, *args, **kwargs):
        """
        Initializes the AttendanceForm and customizes field widgets.

        Sets the date field to render as a date input and filters the user queryset 
        to include only active users.
        """
        super().__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateInput(attrs={'type': 'date'})
        self.fields['user'].queryset = User.objects.filter(is_active=True)


class AttendanceReportForm(forms.Form):
    """
    Form for generating attendance reports based on user and date range.

    This form includes fields to select a user and specify a date range.
    """
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True), 
        required=True, 
        label="Select User"
    )
    from_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="From"
    )
    to_date = forms.DateField(
        required=True, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="To"
    )
