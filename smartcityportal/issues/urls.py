from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.issue_create, name='issue_create'),
    path('my-issues/', views.issue_list, name='issue_list'),
    path('<int:pk>/', views.issue_detail, name='issue_detail'),
    
    # Admin Category Management
    path('admin/categories/', views.IssueCategoryListView.as_view(), name='issue_category_list'),
    path('admin/categories/create/', views.IssueCategoryCreateView.as_view(), name='issue_category_create'),
    path('admin/categories/<int:pk>/edit/', views.IssueCategoryUpdateView.as_view(), name='issue_category_edit'),
    path('admin/categories/<int:pk>/delete/', views.IssueCategoryDeleteView.as_view(), name='issue_category_delete'),
]
