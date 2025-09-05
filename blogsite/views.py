from django.shortcuts import render 
from django.contrib import messages
from blog.models import create_blog


def home(request):
    """Render the home page with latest blog posts"""
    # Get latest 6 blog posts for the home page
    latest_blogs = create_blog.objects.all().order_by('-date')[:6]
    
    return render(request, 'home.html', {'latest_blogs': latest_blogs})

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