from django.shortcuts import render 


def home(request):
    """Render the home page"""
    
    return render(request, 'home.html')

def about(request):
    """Render the about page"""
    return render(request, 'about.html')
def categories(request):
    """Render the Categories page"""
    return render(request, 'categories.html')