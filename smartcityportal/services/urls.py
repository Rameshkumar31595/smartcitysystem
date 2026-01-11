from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='service_list'),
    path('<int:pk>/', views.service_detail, name='service_detail'),
    
    # Admin Category Management
    path('admin/categories/', views.ServiceCategoryListView.as_view(), name='service_category_list'),
    path('admin/categories/create/', views.ServiceCategoryCreateView.as_view(), name='service_category_create'),
    path('admin/categories/<int:pk>/edit/', views.ServiceCategoryUpdateView.as_view(), name='service_category_edit'),
    path('admin/categories/<int:pk>/delete/', views.ServiceCategoryDeleteView.as_view(), name='service_category_delete'),
]
