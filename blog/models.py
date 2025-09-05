from datetime import timezone
from django.db import models

# Create your models here.

class create_blog(models.Model):
    typeofblog=( 'web development', 'programming', 'technology', 'news', 'entertainment', 'sports', 'travel', 'lifestyle','javascripts' )
    title = models.CharField(max_length=200)
    slug=models.SlugField(max_length=200)
    Author_name=models.CharField(max_length=100)
    date=models.DateTimeField(default=timezone.now)
    content=models.TextField()
    image=models.ImageField(upload_to='blog/images')
    Category=models.CharField(max_length=100,choices=typeofblog)