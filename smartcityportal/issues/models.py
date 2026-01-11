from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

class IssueCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Issue(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="issues")
    category = models.ForeignKey(IssueCategory, on_delete=models.CASCADE, related_name="issues")
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to="issue_images/", blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # State machine: allowed transitions
    ALLOWED_TRANSITIONS = {
        Status.OPEN: (Status.IN_PROGRESS, Status.RESOLVED, Status.REJECTED),
        Status.IN_PROGRESS: (Status.RESOLVED, Status.REJECTED),
        Status.RESOLVED: tuple(),
        Status.REJECTED: tuple(),
    }

    def set_status(self, new_status, changed_by, remarks=""):
        if new_status not in self.Status.values:
            raise ValidationError(f"Invalid status: {new_status}")

        # Enforce admin-only changes
        if changed_by is None or (not changed_by.is_staff and not changed_by.is_superuser):
            raise ValidationError("Only administrators can change issue status.")

        if self.status == new_status:
            return  # no change -> no history

        allowed = self.ALLOWED_TRANSITIONS.get(self.status, tuple())
        if new_status not in allowed:
            raise ValidationError(
                f"Invalid transition from {self.get_status_display()} to {self.Status(new_status).label}."
            )

        self.status = new_status
        self.save(update_fields=["status", "updated_at"])
        IssueStatusHistory.objects.create(
            issue=self,
            status=new_status,
            remarks=remarks,
            changed_by=changed_by,
        )

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

class IssueStatusHistory(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name="status_history")
    status = models.CharField(max_length=15, choices=Issue.Status.choices)
    remarks = models.TextField(blank=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="status_changes"
    )
    changed_at = models.DateTimeField(auto_now_add=True)
