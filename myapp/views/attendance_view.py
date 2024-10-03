from django.shortcuts import render
from django.views import View
from ..forms.attendance_forms import AttendanceForm
from ..models.attendance import Attendance

class AttendanceManagementView(View):
    """
    View for managing attendance marking.

    This view handles the display of the attendance form and processes 
    attendance marking for users. It manages messages to inform users 
    about the status of attendance marking.
    """
    
    def get(self, request):
        """
        Handles GET requests to display the attendance management form.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Renders the 'attendance_management.html' template 
            with a fresh attendance form and any messages from the session.
        """
        form = AttendanceForm()
        messages = request.session.get('messages', [])
        request.session['messages'] = []  # Clear messages for fresh state
        return render(request, 'attendance_management.html', {'form': form, 'messages': messages})

    def post(self, request):
        """
        Handles POST requests to process the attendance marking form.

        Validates the form data and either marks attendance for the user
        or informs the user if attendance has already been marked for 
        the specified date.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Renders the 'attendance_management.html' template 
            with the attendance form and status messages.
        """
        form = AttendanceForm(request.POST)
        request.session['messages'] = []  # Clear previous messages

        if form.is_valid():
            # Extract the cleaned data from the form
            user = form.cleaned_data['user']  # The user selected in the form
            date = form.cleaned_data['date']

            # Check if attendance has already been marked for this user and date
            if Attendance.objects.filter(user=user, date=date).exists():
                messages = request.session.get('messages', [])
                messages.append(f"Attendance for {user} on {date} has already been marked.")
                request.session['messages'] = messages
            else:
                # Save the form and mark attendance
                attendance_record = form.save(commit=False)
                attendance_record.marked_by = request.user  # Optional tracking who marked it
                attendance_record.save()
                messages = request.session.get('messages', [])
                messages.append("Attendance marked successfully.")
                request.session['messages'] = messages

            return render(request, 'attendance_management.html', {'form': form, 'messages': messages})

        else:
            # If form is not valid, print the errors
            print(form.errors)
            return render(request, 'attendance_management.html', {'form': form, 'messages': form.errors})
