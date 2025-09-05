from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import create_blog
from .forms import BlogForm

# Create your views here.
def blog_list(request):
    if request.method == 'POST':
        # Handle blog creation
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post created successfully!')
            return redirect('blog_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogForm()
    
    # Get all blog posts
    blogs = create_blog.objects.all().order_by('-date')
    
    return render(request, 'blog/index.html', {
        'blogs': blogs,
        'form': form
    })

def blog_detail(request, slug):
    blog = get_object_or_404(create_blog, slug=slug)
    return render(request, 'blog/detail.html', {'blog': blog})