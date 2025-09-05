"""
URL configuration for blogsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from . import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('ritesh/', views.home, name='home'),
    
    # Additional project-level views
    path('about/', views.AboutView.as_view(), name='about'),
    path('riyesh/', views.RiyeshView.as_view(), name='riyesh'),
    path('contact/', views.contact_view, name='contact'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    
    # API endpoints
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
    path('api/stats/', views.blog_stats, name='blog_stats'),
]

# Custom error handlers
handler404 = 'blogsite.views.handler404'
handler500 = 'blogsite.views.handler500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                         document_root=settings.MEDIA_ROOT)
