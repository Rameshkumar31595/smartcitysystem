from django.contrib import admin
from .models import IssueCategory, Issue, IssueStatusHistory

class IssueStatusHistoryInline(admin.TabularInline):
    model = IssueStatusHistory
    extra = 0
    readonly_fields = ('status', 'remarks', 'changed_by', 'changed_at')

@admin.register(IssueCategory)
class IssueCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'user', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description', 'location')
    ordering = ('-created_at',)
    inlines = [IssueStatusHistoryInline]
