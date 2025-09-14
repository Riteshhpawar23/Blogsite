
from django.urls import path
from . import views

urlpatterns = [
    # Core blog views (local database)
    path('', views.blog_list, name='blog_list'),
    path('detail/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # API-only views (REST API integration)
    path('api-blogs/', views.api_blog_list, name='api_blog_list'),
    path('sync-to-api/', views.sync_blogs_to_api, name='sync_blogs_to_api'),
    
    # Category and search views
    path('category/<str:category>/', views.blog_category, name='blog_category'),
    path('search/', views.blog_search, name='blog_search'),
    path('recent/', views.recent_blogs, name='recent_blogs'),
    
    # CRUD operations
    path('edit/<slug:slug>/', views.blog_edit, name='blog_edit'),
    path('delete/<slug:slug>/', views.blog_delete, name='blog_delete'),
    
    # Utility views
    path('stats/', views.blog_stats, name='blog_stats'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # API endpoints
    path('api/create/', views.api_create_blog, name='api_create_blog'),
    path('api/integration/', views.BlogAPIIntegration.as_view(), name='api_integration'),
]
