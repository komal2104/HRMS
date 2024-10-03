from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home(request):
    """
    Renders the home page for authenticated users.

    This view serves the home page of the application. It is protected 
    by the `login_required` decorator, ensuring that only authenticated 
    users can access this page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'home.html' template.
    """
    return render(request, 'home.html')
