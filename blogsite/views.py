from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from blog.models import Post, Category
from django.db.models import Count

def home_redirect(request):
    """Redirect to blog homepage"""
    return redirect('blog:post_list')

class AboutView(TemplateView):
    """About page view"""
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(status='published').count()
        context['total_categories'] = Category.objects.count()
        return context

def contact_view(request):
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if name and email and subject and message:
            # Here you can add email sending logic
            # send_mail(
            #     f'Contact Form: {subject}',
            #     f'From: {name} <{email}>\n\n{message}',
            #     settings.DEFAULT_FROM_EMAIL,
            #     ['admin@yourblog.com'],
            #     fail_silently=False,
            # )
            messages.success(request, 'Thank you for your message! We\'ll get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')
    
    return render(request, 'contact.html')

def search_suggestions(request):
    """AJAX endpoint for search suggestions"""
    query = request.GET.get('q', '')
    suggestions = []
    
    if query and len(query) >= 2:
        posts = Post.objects.filter(
            title__icontains=query,
            status='published'
        )[:5]
        
        suggestions = [
            {
                'title': post.title,
                'url': post.get_absolute_url(),
                'category': post.category.name
            }
            for post in posts
        ]
    
    return JsonResponse({'suggestions': suggestions})

def blog_stats(request):
    """API endpoint for blog statistics"""
    stats = {
        'total_posts': Post.objects.filter(status='published').count(),
        'total_categories': Category.objects.count(),
        'posts_by_category': list(
            Category.objects.annotate(
                post_count=Count('posts', filter=models.Q(posts__status='published'))
            ).values('name', 'post_count')
        ),
        'recent_posts': [
            {
                'title': post.title,
                'url': post.get_absolute_url(),
                'publish_date': post.publish.isoformat()
            }
            for post in Post.objects.filter(status='published')[:5]
        ]
    }
    return JsonResponse(stats)

class PrivacyPolicyView(TemplateView):
    """Privacy Policy page"""
    template_name = 'privacy.html'

class TermsView(TemplateView):
    """Terms of Service page"""
    template_name = 'terms.html'

def handler404(request, exception):
    """Custom 404 error handler"""
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    return render(request, 'errors/500.html', status=500)