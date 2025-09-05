from django.db import models
from django.utils import timezone

# Create your models here.

class create_blog(models.Model):
    typeofblog = (
        ('web development', 'Web Development'),
        ('programming', 'Programming'),
        ('technology', 'Technology'),
        ('news', 'News'),
        ('entertainment', 'Entertainment'),
        ('sports', 'Sports'),
        ('travel', 'Travel'),
        ('lifestyle', 'Lifestyle'),
        ('javascripts', 'JavaScript'),
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    Author_name = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/images')
    Category = models.CharField(max_length=100, choices=typeofblog)
    
    def __str__(self):
        return self.title