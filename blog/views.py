from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.base import ContentFile
import requests
import json
import base64
from .models import create_blog
from .forms import BlogForm

# REST API Configuration
REST_API_BASE_URL = "http://127.0.0.1:8000/Api/V1"

def send_blog_to_api(blog_instance, image_file=None):
    """
    Send blog data to REST API
    """
    try:
        # Prepare data for API
        data = {
            'title': blog_instance.title,
            'slug': blog_instance.slug,
            'Author_name': blog_instance.Author_name,
            'content': blog_instance.content,
            'Category': blog_instance.Category,
        }
        
        # Handle image file if present
        files = {}
        if image_file:
            files['image'] = (image_file.name, image_file.read(), image_file.content_type)
        
        # Send POST request to REST API
        response = requests.post(
            f"{REST_API_BASE_URL}/blogs/",
            data=data,
            files=files if files else None,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            return True
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"Request Error: {str(e)}")
        return False
    except Exception as e:
        print(f"General Error: {str(e)}")
        return False

def get_blogs_from_api():
    """
    Fetch blogs from REST API
    """
    try:
        response = requests.get(f"{REST_API_BASE_URL}/blogs/", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

# Create your views here.

def blog_list(request):
    """
    Display list of all blog posts with pagination and filtering
    """
    if request.method == 'POST':
        # Handle blog creation - send to REST API
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # Save locally first
            blog_instance = form.save()
            
            # Also send to REST API
            success = send_blog_to_api(blog_instance, request.FILES.get('image'))
            
            if success:
                messages.success(request, 'Blog post created successfully and synced to API!')
            else:
                messages.warning(request, 'Blog post created locally, but failed to sync to API.')
            
            return redirect('blog_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm()
    
    # Get all blog posts from local database
    blogs = create_blog.objects.all().order_by('-date')
    
    # Filter by category if provided
    category = request.GET.get('category')
    if category:
        blogs = blogs.filter(Category__icontains=category)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(Author_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter dropdown
    categories = [choice[0] for choice in create_blog.typeofblog]
    
    return render(request, 'blog/index.html', {
        'page_obj': page_obj,
        'blogs': page_obj,  # For backward compatibility
        'form': form,
        'categories': categories,
        'current_category': category,
        'search_query': search_query,
    })


def blog_detail(request, slug):
    """
    Display detailed view of a single blog post
    """
    blog = get_object_or_404(create_blog, slug=slug)
    
    # Get related blogs (same category, excluding current blog)
    related_blogs = create_blog.objects.filter(
        Category=blog.Category
    ).exclude(id=blog.id).order_by('-date')[:3]
    
    return render(request, 'blog/detail.html', {
        'blog': blog,
        'related_blogs': related_blogs
    })


def blog_category(request, category):
    """
    Display blogs filtered by category
    """
    blogs = create_blog.objects.filter(Category__iexact=category).order_by('-date')
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get category display name
    category_display = dict(create_blog.typeofblog).get(category, category.title())
    
    return render(request, 'blog/category.html', {
        'page_obj': page_obj,
        'blogs': page_obj,
        'category': category,
        'category_display': category_display,
    })


def blog_search(request):
    """
    Handle blog search functionality
    """
    query = request.GET.get('q', '')
    blogs = create_blog.objects.none()
    
    if query:
        blogs = create_blog.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(Author_name__icontains=query)
        ).order_by('-date')
    
    # Pagination
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/search_results.html', {
        'page_obj': page_obj,
        'blogs': page_obj,
        'query': query,
        'total_results': blogs.count()
    })


def recent_blogs(request):
    """
    Get recent blog posts
    """
    limit = request.GET.get('limit', 5)
    try:
        limit = int(limit)
    except ValueError:
        limit = 5
    
    recent_blogs = create_blog.objects.all().order_by('-date')[:limit]
    
    return render(request, 'blog/recent_blogs.html', {
        'recent_blogs': recent_blogs
    })


@csrf_exempt
def api_create_blog(request):
    """
    API endpoint to create blog via AJAX
    """
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            
            # Create blog instance
            blog = create_blog.objects.create(
                title=data.get('title'),
                slug=data.get('slug'),
                Author_name=data.get('Author_name'),
                content=data.get('content'),
                Category=data.get('Category'),
                # Note: image handling would need special treatment for file uploads
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Blog created successfully!',
                'blog_id': blog.id,
                'slug': blog.slug
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error creating blog: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def blog_stats(request):
    """
    Display blog statistics
    """
    total_blogs = create_blog.objects.count()
    categories_stats = {}
    
    for category_key, category_display in create_blog.typeofblog:
        count = create_blog.objects.filter(Category=category_key).count()
        categories_stats[category_key] = {
            'display_name': category_display,
            'count': count
        }
    
    return render(request, 'blog/stats.html', {
        'total_blogs': total_blogs,
        'categories_stats': categories_stats
    })


class BlogAPIIntegration(View):
    """
    Integration with REST API for external data
    """
    
    def get_api_data(self, endpoint):
        """
        Helper method to fetch data from REST API
        """
        try:
            # Assuming your REST API is running on localhost:8000
            api_url = f"http://127.0.0.1:8000/Api/V1/{endpoint}"
            response = requests.get(api_url, timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            pass
        return None
    
    def get(self, request):
        """
        Display API integration page
        """
        # Fetch data from REST API
        api_blogs = self.get_api_data('blogs/')
        api_categories = self.get_api_data('categories/')
        api_stats = self.get_api_data('stats/')
        
        return render(request, 'blog/api_integration.html', {
            'api_blogs': api_blogs,
            'api_categories': api_categories,
            'api_stats': api_stats
        })


def about(request):
    """
    About page view
    """
    return render(request, 'about.html')


def contact(request):
    """
    Contact page view
    """
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # You can add email sending logic here
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'contact.html')


def api_blog_list(request):
    """
    Display blogs from REST API only (for testing API integration)
    """
    if request.method == 'POST':
        # Create blog directly through REST API
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            # Don't save locally, send directly to API
            blog_data = {
                'title': form.cleaned_data['title'],
                'slug': form.cleaned_data['slug'],
                'Author_name': form.cleaned_data['Author_name'],
                'content': form.cleaned_data['content'],
                'Category': form.cleaned_data['Category'],
            }
            
            # Handle image
            files = {}
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                files['image'] = (image_file.name, image_file.read(), image_file.content_type)
            
            try:
                # Send directly to REST API
                response = requests.post(
                    f"{REST_API_BASE_URL}/blogs/",
                    data=blog_data,
                    files=files if files else None,
                    timeout=10
                )
                
                if response.status_code in [200, 201]:
                    messages.success(request, 'Blog post created successfully in REST API!')
                else:
                    messages.error(request, f'Failed to create blog post: {response.status_code}')
                    
            except requests.RequestException as e:
                messages.error(request, f'Error connecting to API: {str(e)}')
            
            return redirect('api_blog_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm()
    
    # Get blogs from REST API
    api_data = get_blogs_from_api()
    blogs = []
    
    if api_data and 'results' in api_data:
        blogs = api_data['results']
    elif api_data and isinstance(api_data, list):
        blogs = api_data
    
    return render(request, 'blog/api_blog_list.html', {
        'blogs': blogs,
        'form': form,
        'api_url': REST_API_BASE_URL
    })


def sync_blogs_to_api(request):
    """
    Sync all local blogs to REST API
    """
    if request.method == 'POST':
        local_blogs = create_blog.objects.all()
        success_count = 0
        error_count = 0
        
        for blog in local_blogs:
            success = send_blog_to_api(blog)
            if success:
                success_count += 1
            else:
                error_count += 1
        
        messages.success(request, f'Sync completed: {success_count} successful, {error_count} errors')
        return redirect('blog_list')
    
    return render(request, 'blog/sync_confirmation.html')