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
    """Render the home page with latest blog posts from API"""
    # Get latest 6 blog posts from API for the home page
    latest_blogs = []
    try:
        api_data = get_blogs_from_api()
        if api_data and 'results' in api_data:
            latest_blogs = api_data['results'][:6]
        elif api_data and isinstance(api_data, list):
            latest_blogs = api_data[:6]
    except:
        # If API fails, show empty list
        latest_blogs = []
    
    return render(request, 'home.html', {
        'latest_blogs': latest_blogs,
        'api_mode': True
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