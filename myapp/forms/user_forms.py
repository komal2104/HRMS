from django import forms
from django.contrib.auth.forms import AuthenticationForm
from ..models.user import User
from ..models.designation import Designation
from ..models.department import Department

class SuperAdminLoginForm(AuthenticationForm):
    """
    Form for super admin login.

    Inherits from Django's AuthenticationForm and includes fields 
    for username and password.
    """
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class UserForm(forms.ModelForm):
    """
    Form for creating or updating user profiles.

    This form includes fields for the user's name, email, designation, 
    department, and date of joining.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'designation', 'department', 'date_of_joining']
        
    designation = forms.ModelChoiceField(queryset=Designation.objects.all())
    department = forms.ModelChoiceField(queryset=Department.objects.all())
