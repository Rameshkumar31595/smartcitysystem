from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import CityService, ServiceCategory
from .forms import ServiceCategoryForm

def is_admin(user):
    return user.is_staff or user.is_superuser or user.role == 'ADMIN'

@login_required
def service_list(request):
    services = CityService.objects.select_related('category').all()
    categories = ServiceCategory.objects.all()
    
    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        services = services.filter(category_id=category_id)
    
    # Search by name or description
    search_query = request.GET.get('q') or request.GET.get('search')
    if search_query:
        services = services.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    context = {
        'services': services,
        'categories': categories,
        'selected_category': category_id,
        'search_query': search_query or '',
    }
    return render(request, 'services/service_list.html', context)

@login_required
def service_detail(request, pk):
    service = get_object_or_404(CityService.objects.select_related('category'), pk=pk)
    return render(request, 'services/service_detail.html', {'service': service})

# Admin-only Category Management Views
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return is_admin(self.request.user)

class ServiceCategoryListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'admin/service_categories_list.html'
    context_object_name = 'categories'
    ordering = ['name']

class ServiceCategoryCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'admin/service_category_form.html'
    success_url = reverse_lazy('service_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Service category created successfully!')
        return super().form_valid(form)

class ServiceCategoryUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'admin/service_category_form.html'
    success_url = reverse_lazy('service_category_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Service category updated successfully!')
        return super().form_valid(form)

class ServiceCategoryDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = ServiceCategory
    template_name = 'admin/service_category_confirm_delete.html'
    success_url = reverse_lazy('service_category_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Service category deleted successfully!')
        return super().delete(request, *args, **kwargs)
