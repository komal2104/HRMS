from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from ..forms.user_forms import SuperAdminLoginForm
from django.contrib.auth import authenticate, login

def user_logout(request):
    """
    Logs out the current user and redirects them to the super admin login page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: A redirect to the 'super_admin_login' URL.
    """
    logout(request)  # Log out the user
    return redirect('super_admin_login')  # Redirect to the login page


def super_admin_login(request):
    """
    Handles the super admin login process.

    If the request method is POST, it validates the login form and attempts 
    to authenticate the user. If successful, the user is logged in and 
    redirected to the home page. If the request method is GET, it displays 
    a fresh login form.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'login.html' template with the login form 
        or redirects to the home page upon successful login.
    """
    if request.method == 'POST':
        form = SuperAdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to the home page
    else:
        form = SuperAdminLoginForm()  # Create a new form for GET request

    return render(request, 'login.html', {'form': form})  # Render the login form
