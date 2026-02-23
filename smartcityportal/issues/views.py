from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Issue, IssueCategory
from .forms import IssueForm, IssueCategoryForm

def is_admin(user):
    return user.is_staff or user.is_superuser or user.role == 'ADMIN'

@login_required
def issue_create(request):
	if request.method == 'POST':
		form = IssueForm(request.POST, request.FILES)
		if form.is_valid():
			issue = form.save(commit=False)
			issue.user = request.user
			issue.save()
			messages.success(request, 'Issue reported successfully!')
			return redirect('issue_detail', pk=issue.pk)
	else:
		form = IssueForm()
	return render(request, 'issues/issue_create.html', {'form': form})

@login_required
def issue_list(request):
	issues = Issue.objects.filter(user=request.user).select_related('category').order_by('-created_at')
    
	# Filter by status
	status_filter = request.GET.get('status')
	if status_filter:
		issues = issues.filter(status=status_filter)
    
	context = {
		'issues': issues,
		'status_choices': Issue.Status.choices,
		'selected_status': status_filter,
	}
	return render(request, 'issues/issue_list.html', context)

@login_required
def issue_detail(request, pk):
	issue = get_object_or_404(Issue.objects.select_related('category', 'user'), pk=pk, user=request.user)
	status_history = issue.status_history.select_related('changed_by').order_by('-changed_at')
	context = {
		'issue': issue,
		'status_history': status_history,
	}
	return render(request, 'issues/issue_detail.html', context)

# Admin-only Category Management Views
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)

class IssueCategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = IssueCategory
    template_name = 'admin/issue_categories_list.html'
    context_object_name = 'categories'
    ordering = ['name']

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
        return qs

class IssueCategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = IssueCategory
    form_class = IssueCategoryForm
    template_name = 'admin/issue_category_form.html'
    success_url = reverse_lazy('issue_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Issue category created successfully!')
        return super().form_valid(form)

class IssueCategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = IssueCategory
    form_class = IssueCategoryForm
    template_name = 'admin/issue_category_form.html'
    success_url = reverse_lazy('issue_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Issue category updated successfully!')
        return super().form_valid(form)

class IssueCategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = IssueCategory
    template_name = 'admin/issue_category_confirm_delete.html'
    success_url = reverse_lazy('issue_category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Issue category deleted successfully!')
        return super().delete(request, *args, **kwargs)
