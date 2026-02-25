from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, AdminActivityLog

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'first_name', 'last_name', 'email'),
        }),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


@admin.register(AdminActivityLog)
class AdminActivityLogAdmin(admin.ModelAdmin):
    list_display = ('admin', 'action_type', 'description', 'timestamp')
    list_filter = ('action_type', 'timestamp')
    search_fields = ('admin__username', 'description', 'target_info')
    readonly_fields = ('admin', 'action_type', 'description', 'target_model', 'target_id', 'target_info', 'ip_address', 'timestamp')
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        # Prevent manual creation of logs - they should only be created programmatically
        return False
    
    def has_change_permission(self, request, obj=None):
        # Logs should be immutable
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Allow superusers to delete old logs if needed
        return request.user.is_superuser
