from django.contrib.auth.decorators import login_required
from ..models.user import User
from django.core.paginator import Paginator
from ..forms.user_forms import UserForm
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q

@login_required
def user_list(request):
    """
    Displays a paginated list of active users, with optional search and sorting.

    Users can be searched by name or email, and the list can be sorted based 
    on specified fields. The results are paginated to show a limited number 
    of users per page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'user_list.html' template with the list of 
        users, search query, and sorting options.
    """
    search_query = request.GET.get('search', '')
    sort_order = request.GET.get('order', 'asc') 
    sort_by = request.GET.get('sortby', 'name')

    users = User.objects.filter(
        Q(name__icontains=search_query) | Q(email__icontains=search_query),
        is_active=True
    )
    paginator = Paginator(users, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)

    return render(request, 'user_list.html', {
        'users': users,
        'search_query': search_query,
        'sort_by': sort_by.lstrip('-'),  
        'sort_order': 'asc',  
    })

@login_required
def user_add(request):
    """
    Handles the addition of a new user through a form submission.

    If the request method is POST, it validates the form data and saves 
    the new user to the database. If the request method is GET, it 
    displays a blank form for user input.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Renders the 'user_form.html' template with the user 
        form, or redirects to the user list upon successful addition.
    """
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_edit(request, user_id):
    """
    Handles the editing of an existing user's details.

    Retrieves the user based on the provided user ID. If the request 
    method is POST, it validates the form data and updates the user's 
    details. If the request method is GET, it displays the current 
    details in the form for editing.

    Args:
        request: The HTTP request object.
        user_id: The ID of the user to be edited.

    Returns:
        HttpResponse: Renders the 'user_form.html' template with the 
        user form pre-populated with the existing user's data, or 
        redirects to the user list upon successful edit.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

@login_required
def user_delete(request, user_id):
    """
    Marks a user as inactive (deleted) without removing them from the database.

    Retrieves the user based on the provided user ID, sets their 
    is_active status to False, and saves the changes to the database.

    Args:
        request: The HTTP request object.
        user_id: The ID of the user to be deleted.

    Returns:
        HttpResponse: Redirects to the user list after marking the user 
        as inactive.
    """
    user = get_object_or_404(User, id=user_id)
    user.is_active = False  # Mark the user as inactive
    user.save()
    return redirect('user_list')
