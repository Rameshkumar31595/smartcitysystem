from django import forms
from .models import ServiceCategory, CityService

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
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

class CityServiceForm(forms.ModelForm):
    class Meta:
        model = CityService
        fields = ['category', 'name', 'description', 'contact_info']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description',
                'rows': 4
            }),
            'contact_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter contact details',
                'rows': 3
            }),
        }
