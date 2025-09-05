from django.shortcuts import render 
from django.contrib import messages


def home(request):
    """Render the home page"""
    
    return render(request, 'home.html')

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