from django.shortcuts import render 
from django.contrib import messages
import requests

# REST API Configuration
REST_API_BASE_URL = "http://127.0.0.1:8000/Api/V1"

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

def home(request):
    """Render the home page with latest blog posts from API or local database"""
    # Import local blog model for fallback
    from blog.models import create_blog
    
    # Get latest 6 blog posts from API for the home page
    latest_blogs = []
    api_mode = True
    
    try:
        api_data = get_blogs_from_api()
        if api_data and 'results' in api_data:
            latest_blogs = api_data['results'][:6]
        elif api_data and isinstance(api_data, list):
            latest_blogs = api_data[:6]
        
        # Process image URLs for each blog
        for blog in latest_blogs:
            if blog.get('image') and not blog.get('image_url'):
                image_path = blog['image']
                if image_path.startswith('/'):
                    blog['image_url'] = f"http://127.0.0.1:8000{image_path}"
                elif not image_path.startswith('http'):
                    blog['image_url'] = f"http://127.0.0.1:8000/media/{image_path}"
                else:
                    blog['image_url'] = image_path
    except:
        # If API fails, fall back to local database
        api_mode = False
        try:
            latest_blogs = list(create_blog.objects.all().order_by('-date')[:6])
        except:
            latest_blogs = []
    
    # Set featured post (first blog if available)
    featured_post = latest_blogs[0] if latest_blogs else None
    
    return render(request, 'home.html', {
        'latest_blogs': latest_blogs,
        'featured_post': featured_post,
        'api_mode': api_mode
    })

def about(request):
    """Render the about page"""
    return render(request, 'about.html')
    
def categories(request):
    """Render the Categories page"""
    return render(request, 'categories.html')

def contact(request):
    """Render the contact page and handle form submissions"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # You can add logic here to save to database or send email
        # For now, we'll just show a success message
        messages.success(request, f'Thank you {name}! Your message has been received. We will get back to you soon.')
        
    return render(request, 'contact.html')