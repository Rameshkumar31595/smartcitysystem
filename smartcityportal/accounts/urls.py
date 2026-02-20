from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirect/', views.login_redirect, name='login_redirect'),
    path('home/', views.user_home, name='user_home'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_user_list, name='admin_user_list'),
    path('admin/users/create/', views.admin_user_create, name='admin_user_create'),
    path('admin/users/<int:pk>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('admin/users/<int:pk>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('admin/users/<int:pk>/delete-confirm/', views.admin_user_delete_confirm, name='admin_user_delete_confirm'),
    path('admin/users/<int:pk>/role/', views.admin_user_update_role, name='admin_user_update_role'),
    path('admin/issues/', views.admin_issue_list, name='admin_issue_list'),
    path('admin/issues/<int:pk>/', views.admin_issue_detail, name='admin_issue_detail'),
    path('admin/issues/<int:pk>/delete/', views.admin_issue_delete, name='admin_issue_delete'),
]
