from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirect/', views.login_redirect, name='login_redirect'),
    path('home/', views.user_home, name='user_home'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/password/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/profile/'
    ), name='password_change'),
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        success_url='/accounts/password_reset/done/',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/accounts/reset/done/'
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

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
    path('admin/activity-logs/', views.admin_activity_logs, name='admin_activity_logs'),
]
