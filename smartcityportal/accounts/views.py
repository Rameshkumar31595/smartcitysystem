from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
import logging
from issues.models import Issue, IssueStatusHistory
from .forms import SignUpForm, AdminUserCreateForm, AdminUserEditForm, UserProfileForm

# Set up logging for signup and admin actions
logger = logging.getLogger('accounts')

User = get_user_model()

def is_admin(user):
    return user.is_staff or user.is_superuser or user.role == 'ADMIN'

def home_router(request):
    """Smart home routing - landing for anonymous, dashboard for authenticated"""
    if request.user.is_authenticated:
        # Redirect authenticated users to their dashboard
        if is_admin(request.user):
            return redirect('admin_dashboard')
        else:
            return redirect('user_home')
    # Show landing page for anonymous users
    return render(request, 'landing.html')

def signup(request):
    """Handle user registration with proper validation and logging."""
    if request.user.is_authenticated:
        return redirect('home')  # Use home router for authenticated users
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Log successful account creation for audit trail
                logger.info(f'New account created: username={user.username}, email={user.email}')
                messages.success(request, 'Account created successfully! Please sign in.')
                return redirect('login')
            except Exception as e:
                # Log any database errors during signup
                logger.error(f'Error creating account: {str(e)}')
                messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            # Log form validation errors (don't expose details to user)
            logger.debug(f'Signup form validation failed: {form.errors}')
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

@login_required
def login_redirect(request):
    """Redirect users based on their role after login"""
    if is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('issue_list')

@login_required
def user_home(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    return render(request, 'dashboard/user_home.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Statistics
    total_issues = Issue.objects.count()
    open_issues = Issue.objects.filter(status=Issue.Status.OPEN).count()
    in_progress_issues = Issue.objects.filter(status=Issue.Status.IN_PROGRESS).count()
    resolved_issues = Issue.objects.filter(status=Issue.Status.RESOLVED).count()
    rejected_issues = Issue.objects.filter(status=Issue.Status.REJECTED).count()
    
    # Recent issues
    recent_issues = Issue.objects.select_related('user', 'category').order_by('-created_at')[:10]
    
    context = {
        'total_issues': total_issues,
        'open_issues': open_issues,
        'in_progress_issues': in_progress_issues,
        'resolved_issues': resolved_issues,
        'rejected_issues': rejected_issues,
        'recent_issues': recent_issues,
    }
    return render(request, 'dashboard/admin_home.html', context)

@login_required
@user_passes_test(is_admin)
def admin_issue_list(request):
    issues = Issue.objects.select_related('user', 'category').order_by('-created_at')
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        issues = issues.filter(status=status_filter)
    
    # Search
    search_query = request.GET.get('search')
    if search_query:
        issues = issues.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(location__icontains=search_query)
        )
    
    context = {
        'issues': issues,
        'status_choices': Issue.Status.choices,
        'selected_status': status_filter,
        'search_query': search_query or '',
    }
    return render(request, 'dashboard/admin_issue_list.html', context)

@login_required
@user_passes_test(is_admin)
def admin_issue_detail(request, pk):
    issue = get_object_or_404(Issue.objects.select_related('user', 'category'), pk=pk)
    status_history = issue.status_history.select_related('changed_by').order_by('-changed_at')
    allowed_status_values = Issue.ALLOWED_TRANSITIONS.get(issue.status, tuple())
    allowed_status_choices = [(value, label) for value, label in Issue.Status.choices if value in allowed_status_values]
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        remarks = request.POST.get('remarks', '')
        try:
            issue.set_status(new_status, request.user, remarks)
        except ValidationError as exc:
            messages.error(request, exc.message)
        else:
            messages.success(request, f'Issue status updated to {issue.get_status_display()}')
            return redirect('admin_issue_detail', pk=pk)
    
    context = {
        'issue': issue,
        'status_history': status_history,
        'status_choices': Issue.Status.choices,
        'allowed_status_choices': allowed_status_choices,
    }
    return render(request, 'dashboard/admin_issue_detail.html', context)


@login_required
@user_passes_test(is_admin)
def admin_issue_delete(request, pk):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('user_home')

    if request.method != 'POST':
        return redirect('admin_issue_detail', pk=pk)

    issue = get_object_or_404(Issue, pk=pk)
    issue.delete()
    messages.success(request, 'Issue deleted successfully.')
    return redirect('admin_issue_list')


@login_required
@user_passes_test(is_admin)
def admin_user_list(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect('user_home')

    form = SignUpForm()
    users = User.objects.all()
    q = request.GET.get('q', '').strip()
    if q:
        users = users.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q) | Q(email__icontains=q))
    users = users.order_by('username')
    
    context = {
        'users': users,
        'form': form,
    }
    return render(request, 'dashboard/admin_user_list.html', context)


@login_required
@user_passes_test(is_admin)
def admin_user_create(request):
    """Allow admin to create new users with full control over role and permissions."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('You do not have permission to access this page.')

    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f'New user created by admin: username={user.username}, by={request.user.username}')
            messages.success(request, f'User "{user.username}" created successfully.')
            return redirect('admin_user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
            logger.debug(f'User creation form validation failed: {form.errors}')
    else:
        form = AdminUserCreateForm()

    context = {
        'form': form,
        'is_create': True,
    }
    return render(request, 'dashboard/admin_user_form.html', context)


@login_required
@user_passes_test(is_admin)
def admin_user_delete(request, pk):
    """Delete user after POST confirmation (redirects to confirmation page on GET)."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('You do not have permission to access this page.')

    if request.method != 'POST':
        return redirect('admin_user_delete_confirm', pk=pk)

    user_obj = get_object_or_404(User, pk=pk)
    if user_obj == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_user_list')

    username = user_obj.username
    user_obj.delete()
    logger.info(f'User deleted by admin: username={username}, by={request.user.username}')
    messages.success(request, f'User "{username}" deleted successfully.')
    return redirect('admin_user_list')


@login_required
@user_passes_test(is_admin)
def admin_user_edit(request, pk):
    """Allow admin to edit user details, role, and permissions."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('You do not have permission to access this page.')

    user_obj = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = AdminUserEditForm(request.POST, instance=user_obj)
        if form.is_valid():
            # Prevent self-demotion
            if user_obj == request.user and not request.POST.get('is_staff'):
                messages.error(request, 'You cannot remove your own admin privileges.')
            else:
                form.save()
                logger.info(f'User edited: username={user_obj.username}, by={request.user.username}')
                messages.success(request, f'User "{user_obj.username}" updated successfully.')
                return redirect('admin_user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AdminUserEditForm(instance=user_obj)

    context = {
        'form': form,
        'edit_user': user_obj,
    }
    return render(request, 'dashboard/admin_user_form.html', context)


@login_required
@user_passes_test(is_admin)
def admin_user_delete_confirm(request, pk):
    """Show confirmation page before deleting a user."""
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseForbidden('You do not have permission to access this page.')

    user_obj = get_object_or_404(User, pk=pk)

    if user_obj == request.user:
        messages.error(request, 'You cannot delete your own account.')
        return redirect('admin_user_list')

    if request.method == 'POST':
        # User confirmed deletion
        username = user_obj.username
        user_obj.delete()
        logger.info(f'User deleted: username={username}, by={request.user.username}')
        messages.success(request, f'User "{username}" has been deleted.')
        return redirect('admin_user_list')

    context = {'user_to_delete': user_obj}
    return render(request, 'dashboard/admin_user_delete_confirm.html', context)


@login_required
@user_passes_test(is_admin)
def admin_user_update_role(request, pk):
    """Deprecated: Use admin_user_edit instead. Kept for backward compatibility."""
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('user_home')

    if request.method != 'POST':
        return redirect('admin_user_list')

    user_obj = get_object_or_404(User, pk=pk)
    make_admin = request.POST.get('make_admin') == '1'

    if user_obj == request.user and not make_admin:
        messages.error(request, 'You cannot remove your own admin privileges.')
        return redirect('admin_user_list')

    if make_admin:
        user_obj.is_staff = True
        user_obj.role = User.Roles.ADMIN
    else:
        user_obj.is_staff = False
        if not user_obj.is_superuser:
            user_obj.role = User.Roles.USER

    user_obj.save(update_fields=['is_staff', 'role'])
    messages.success(request, f'Role updated for "{user_obj.username}".')
    return redirect('admin_user_list')

@login_required
def profile_view(request):
    """View for users to manage their personal profile."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/profile.html', context)
