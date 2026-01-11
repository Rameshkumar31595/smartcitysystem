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
    path('admin/issues/', views.admin_issue_list, name='admin_issue_list'),
    path('admin/issues/<int:pk>/', views.admin_issue_detail, name='admin_issue_detail'),
]
