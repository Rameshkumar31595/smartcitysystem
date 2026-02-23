"""
URL configuration for smartcityportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from accounts.views import home_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_router, name='home'),
    path('accounts/', include('accounts.urls')),
    path('services/', include('services.urls')),
    path('issues/', include('issues.urls')),
    path('compliance/', TemplateView.as_view(template_name='pages/compliance.html'), name='compliance'),
    path('privacy-policy/', TemplateView.as_view(template_name='pages/privacy_policy.html'), name='privacy_policy'),
    path('terms-of-service/', TemplateView.as_view(template_name='pages/terms_of_service.html'), name='terms_of_service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
