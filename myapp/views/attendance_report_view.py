from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
import openpyxl
from datetime import timedelta
import base64
from django.http import JsonResponse
from io import BytesIO
from ..forms.attendance_forms import AttendanceReportForm
from ..models.attendance import Attendance

class AttendanceReportView(View):
    """
    View for generating attendance reports.

    This view handles the display of the attendance report form and 
    processes the form submission to generate an Excel report 
    based on user attendance.
    """
    
    def get(self, request):
        """
        Handles GET requests to display the attendance report form.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponse: Renders the 'attendance_report.html' template 
            with an empty report form.
        """
        report_form = AttendanceReportForm()  # Create a report form
        return render(request, 'attendance_report.html', {'report_form': report_form})
    
    def post(self, request):
        """
        Handles POST requests to process the attendance report form.

        Validates the form data, fetches attendance records for the specified user 
        and date range, and generates an Excel file containing the attendance report.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response containing the Base64 encoded Excel file 
            and its name, or re-renders the form with errors if invalid.
        """
        report_form = AttendanceReportForm(request.POST)

        if report_form.is_valid():
            user = report_form.cleaned_data['user']
            from_date = report_form.cleaned_data['from_date']
            to_date = report_form.cleaned_data['to_date']
            
            # Fetch attendance data for the date range
            attendance_data = self.get_attendance_data(user, from_date, to_date)
            
            # Generate and export Excel file in memory
            excel_file = self.generate_attendance_report_excel(user, attendance_data, from_date, to_date)
            
            # Encode the Excel file to Base64
            encoded_file = base64.b64encode(excel_file.getvalue()).decode('utf-8')
            
            # Return the Base64 string as a JSON response
            return JsonResponse({
                'file_name': f'attendance_report_{user.name}.xlsx',
                'file_data': encoded_file
            })

        return render(request, 'attendance_report.html', {'report_form': report_form})

    def get_attendance_data(self, user, from_date, to_date):
        """
        Fetches the attendance data for the user for the given date range.

        Args:
            user: The user for whom attendance data is being fetched.
            from_date: The start date of the attendance period.
            to_date: The end date of the attendance period.

        Returns:
            list: A list of dictionaries containing attendance status 
            for each date in the specified range.
        """
        attendance_data = []
        
        # Generate date range
        current_date = from_date
        while current_date <= to_date:
            attendance_entry = Attendance.objects.filter(user=user, date=current_date).first()
            
            if attendance_entry:
                status = 'Present'
            else:
                status = 'Absent'
            
            attendance_data.append({
                'date': current_date,
                'status': status
            })
            
            # Move to the next day
            current_date += timedelta(days=1)
        
        return attendance_data

    def generate_attendance_report_excel(self, user, attendance_data, from_date, to_date):
        """
        Generates an Excel file based on the attendance data in memory.

        Args:
            user: The user for whom the attendance report is generated.
            attendance_data: The list of attendance records.
            from_date: The start date of the attendance period.
            to_date: The end date of the attendance period.

        Returns:
            BytesIO: A BytesIO object containing the Excel file.
        """
        output = BytesIO()
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = f"Attendance Report ({user.name})"
        
        # Add header
        sheet['A1'] = 'Date'
        sheet['B1'] = 'Attendance'
        
        # Add attendance data to the Excel sheet
        row_num = 2
        for entry in attendance_data:
            sheet[f'A{row_num}'] = entry['date'].strftime('%Y-%m-%d')
            sheet[f'B{row_num}'] = entry['status']
            row_num += 1
        
        # Save the workbook to the BytesIO object
        workbook.save(output)
        output.seek(0)  # Go to the start of the BytesIO object
        
        return output
