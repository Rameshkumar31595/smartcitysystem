from django import forms
from .models import Issue, IssueCategory

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ['category', 'title', 'description', 'location', 'image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class IssueCategoryForm(forms.ModelForm):
    class Meta:
        model = IssueCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description (optional)',
                'rows': 4
            }),
        }
