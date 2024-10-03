from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from ..models.user import User

@login_required
def employee_distribution(request):
    """
    View function to aggregate and return the number of active users 
    by department as a JSON response.

    The function iterates through active users, counting them by their 
    associated department. If a user does not belong to a department, 
    they are counted under "No Department".

    Args:
        request: The HTTP request object.

    Returns:
        JsonResponse: A JSON response containing the count of users 
        in each department.
    """
    departments = {}
    
    # Aggregate user count by department
    for user in User.objects.filter(is_active=True):
        department_name = user.department.name if user.department else "No Department"
        if department_name in departments:
            departments[department_name] += 1
        else:
            departments[department_name] = 1
    
    return JsonResponse(departments)

@login_required
def employee_distribution_page(request):
    """
    View function to render the employee department report page.

    This function handles the rendering of the 'employee_dept_report.html' 
    template for displaying employee distribution by department.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A response object rendering the employee 
        department report template.
    """
    return render(request, 'employee_dept_report.html')
