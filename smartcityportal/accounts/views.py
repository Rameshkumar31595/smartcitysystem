from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.core.exceptions import ValidationError
from issues.models import Issue, IssueStatusHistory
from .forms import SignUpForm

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
    if request.user.is_authenticated:
        return redirect('home')  # Use home router for authenticated users
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Account created successfully! Welcome, {username}!')
            return redirect('home')  # HomeRouter will redirect based on role
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
