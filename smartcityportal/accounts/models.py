from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "USER", "User"
        ADMIN = "ADMIN", "Admin"
    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.USER,
    )


class AdminActivityLog(models.Model):
    """
    Model to track admin actions for transparency and audit purposes.
    Logs activities like deleting issues, changing user roles, etc.
    """
    class ActionType(models.TextChoices):
        DELETE_ISSUE = "DELETE_ISSUE", "Deleted Issue"
        DELETE_USER = "DELETE_USER", "Deleted User"
        CREATE_USER = "CREATE_USER", "Created User"
        UPDATE_USER = "UPDATE_USER", "Updated User"
        CHANGE_USER_ROLE = "CHANGE_USER_ROLE", "Changed User Role"
        OTHER = "OTHER", "Other Action"

    admin = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="admin_activities",
        help_text="The administrator who performed the action"
    )
    action_type = models.CharField(
        max_length=20, 
        choices=ActionType.choices,
        help_text="Type of action performed"
    )
    description = models.TextField(
        help_text="Detailed description of the action"
    )
    target_model = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Model affected by the action (e.g., Issue, User)"
    )
    target_id = models.IntegerField(
        null=True, 
        blank=True,
        help_text="ID of the affected object"
    )
    target_info = models.TextField(
        blank=True,
        help_text="Additional information about the target (e.g., issue title, username)"
    )
    ip_address = models.GenericIPAddressField(
        null=True, 
        blank=True,
        help_text="IP address of the admin"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="When the action was performed"
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Admin Activity Log"
        verbose_name_plural = "Admin Activity Logs"

    def __str__(self):
        admin_name = self.admin.username if self.admin else "Unknown"
        return f"{admin_name} - {self.get_action_type_display()} at {self.timestamp}"
