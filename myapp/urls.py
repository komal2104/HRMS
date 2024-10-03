from django.urls import path
from .views.home_view import home
from .views.auth_view import super_admin_login, user_logout
from .views.employee_view import user_list, user_add, user_edit, user_delete
from .views.attendance_view import AttendanceManagementView
from .views.attendance_report_view import AttendanceReportView
from .views.analytics_view import employee_distribution, employee_distribution_page

urlpatterns = [
    path('', super_admin_login, name='super_admin_login'),  # Redirect to login on the root URL
    path('home/', home, name='home'),  # Home page for authenticated users
    path('super-admin/login/', super_admin_login, name='super_admin_login'),  # Super admin login page
    path('logout/', user_logout, name='logout'),  # User logout path
    path('users/', user_list, name='user_list'),  # List of users
    path('users/add/', user_add, name='user_add'),  # Page to add a new user
    path('users/edit/<int:user_id>/', user_edit, name='user_edit'),  # Page to edit user details
    path('users/delete/<int:user_id>/', user_delete, name='user_delete'),  # Path to delete a user
    path('attendance/', AttendanceManagementView.as_view(), name='mark_attendance'),  # Attendance management page
    path('attendance-report/', AttendanceReportView.as_view(), name='attendance_report'),  # Attendance report page
    path('employee-distribution/', employee_distribution, name='employee_distribution'),  # Employee distribution data
    path('employee-distribution-page/', employee_distribution_page, name='employee_distribution_page'),  # Page for employee distribution report
]
