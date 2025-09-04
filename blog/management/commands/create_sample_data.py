from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Category, Tag, Post
from django.utils import timezone
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Create sample blog data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample blog data...')

        # Create categories
        categories_data = [
            {'name': 'Technology', 'description': 'Latest tech news and tutorials'},
            {'name': 'Travel', 'description': 'Travel experiences and guides'},
            {'name': 'Food', 'description': 'Recipes and food reviews'},
            {'name': 'Lifestyle', 'description': 'Tips for better living'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'slug': slugify(cat_data['name']),
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create tags
        tags_data = ['python', 'django', 'web-development', 'tutorial', 'beginner', 
                    'advanced', 'tips', 'guide', 'review', 'news']

        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name,
                defaults={'slug': slugify(tag_name)}
            )
            if created:
                self.stdout.write(f'Created tag: {tag.name}')

        # Get or create author
        author, created = User.objects.get_or_create(
            username='blogauthor',
            defaults={
                'first_name': 'Blog',
                'last_name': 'Author',
                'email': 'author@example.com'
            }
        )

        # Create sample posts
        posts_data = [
            {
                'title': 'Getting Started with Django',
                'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

Django follows the model-template-views architectural pattern. It is maintained by the Django Software Foundation, an independent organization established in the US as a 501 non-profit.

In this post, we'll explore the basics of Django and how to get started with your first project.

## Why Django?

Django comes with several advantages:
- **Fast Development**: Django's "batteries-included" philosophy means you get a lot of functionality out of the box
- **Security**: Django takes security seriously and helps developers avoid common security mistakes
- **Scalable**: Django is used by some of the world's busiest websites
- **Versatile**: You can build almost any type of website with Django

## Getting Started

To start with Django, you'll need Python installed on your system. Then you can install Django using pip:

```bash
pip install Django
```

After installation, you can create your first Django project:

```bash
django-admin startproject myproject
```

This creates a new Django project with the basic structure you need to get started.''',
                'excerpt': 'Learn the basics of Django web framework and how to create your first project.',
                'category': 'Technology',
                'tags': ['python', 'django', 'web-development', 'tutorial', 'beginner']
            },
            {
                'title': 'Top 5 Travel Destinations for 2025',
                'content': '''Planning your next vacation? Here are the top 5 travel destinations that should be on your list for 2025.

## 1. Japan
Japan offers a perfect blend of traditional culture and modern innovation. From the bustling streets of Tokyo to the serene temples of Kyoto, there's something for every traveler.

## 2. Iceland
Known for its stunning natural landscapes, Iceland is perfect for those seeking adventure. Experience the Northern Lights, geysers, and dramatic waterfalls.

## 3. New Zealand
With its diverse landscapes ranging from beaches to mountains, New Zealand is an outdoor enthusiast's paradise.

## 4. Portugal
Portugal offers beautiful coastlines, historic cities, and delicious cuisine at affordable prices.

## 5. Costa Rica
Perfect for eco-tourism, Costa Rica boasts incredible biodiversity and adventure activities.

Each of these destinations offers unique experiences that will create lasting memories. Start planning your 2025 adventure today!''',
                'excerpt': 'Discover the top 5 must-visit travel destinations for your 2025 vacation plans.',
                'category': 'Travel',
                'tags': ['travel', 'guide', 'tips']
            },
            {
                'title': '10-Minute Healthy Breakfast Ideas',
                'content': '''Starting your day with a nutritious breakfast doesn't have to be time-consuming. Here are some quick and healthy breakfast ideas that you can prepare in just 10 minutes.

## 1. Overnight Oats
Prepare the night before by mixing oats with milk, yogurt, and your favorite toppings. In the morning, just grab and go!

## 2. Avocado Toast
Mash half an avocado on whole grain toast, add a pinch of salt, pepper, and a squeeze of lemon.

## 3. Greek Yogurt Parfait
Layer Greek yogurt with berries and granola for a protein-packed breakfast.

## 4. Smoothie Bowl
Blend frozen fruits with a little liquid, pour into a bowl, and top with nuts and seeds.

## 5. Egg Scramble
Quick scrambled eggs with vegetables can be ready in minutes and provide excellent protein.

Remember, a good breakfast sets the tone for the entire day. These options are not only quick but also nutritious and delicious!''',
                'excerpt': 'Quick and nutritious breakfast ideas that take only 10 minutes to prepare.',
                'category': 'Food',
                'tags': ['food', 'healthy', 'tips', 'quick']
            },
            {
                'title': 'The Art of Minimalist Living',
                'content': '''Minimalism isn't about living with nothing; it's about living with intention. It's a lifestyle that helps you focus on what truly matters by eliminating excess.

## What is Minimalism?
Minimalism is the practice of intentionally reducing possessions and commitments to focus on what adds value to your life.

## Benefits of Minimalist Living
- **Less Stress**: Fewer possessions mean less to maintain and organize
- **More Freedom**: Less stuff means more mobility and flexibility
- **Better Focus**: With fewer distractions, you can focus on what's important
- **Financial Benefits**: Buying less saves money

## How to Start
1. **Start Small**: Begin with one area, like your desk or closet
2. **Ask Questions**: Does this item add value to my life?
3. **Quality over Quantity**: Invest in fewer, higher-quality items
4. **Digital Minimalism**: Apply minimalist principles to your digital life too

## Common Misconceptions
Minimalism doesn't mean living in empty spaces or depriving yourself. It's about being intentional with your choices and keeping only what serves a purpose in your life.

The goal is to create space for experiences, relationships, and personal growth rather than accumulating material possessions.''',
                'excerpt': 'Discover how minimalist living can reduce stress and increase focus in your daily life.',
                'category': 'Lifestyle',
                'tags': ['lifestyle', 'minimalism', 'tips', 'guide']
            },
            {
                'title': 'Building Your First REST API with Django',
                'content': '''REST APIs are essential for modern web development. Django REST Framework makes it easy to build powerful and flexible APIs.

## What is a REST API?
REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use standard HTTP methods to perform operations on resources.

## Django REST Framework
Django REST Framework (DRF) is a powerful toolkit for building REST APIs in Django. It provides:
- Serialization for converting complex data types
- Authentication and permissions
- ViewSets and routers for URL routing
- Browsable API for easy testing

## Getting Started
First, install Django REST Framework:

```bash
pip install djangorestframework
```

Add it to your Django settings:

```python
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
]
```

## Creating Your First API
1. **Define Models**: Create Django models for your data
2. **Create Serializers**: Convert model instances to JSON
3. **Write Views**: Handle API requests and responses
4. **Configure URLs**: Set up URL patterns for your API endpoints

## Best Practices
- Use proper HTTP status codes
- Implement proper error handling
- Add authentication and permissions
- Document your API
- Version your API for backward compatibility

Building REST APIs with Django is straightforward once you understand the concepts. Start with a simple API and gradually add more features as needed.''',
                'excerpt': 'Learn how to build your first REST API using Django REST Framework.',
                'category': 'Technology',
                'tags': ['python', 'django', 'api', 'tutorial', 'advanced']
            }
        ]

        for post_data in posts_data:
            # Get category
            category = Category.objects.get(name=post_data['category'])
            
            # Create post
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'slug': slugify(post_data['title']),
                    'author': author,
                    'category': category,
                    'content': post_data['content'],
                    'excerpt': post_data['excerpt'],
                    'status': 'published',
                    'publish': timezone.now()
                }
            )
            
            if created:
                # Add tags
                for tag_name in post_data['tags']:
                    try:
                        tag = Tag.objects.get(name=tag_name)
                        post.tags.add(tag)
                    except Tag.DoesNotExist:
                        # Create tag if it doesn't exist
                        tag = Tag.objects.create(name=tag_name, slug=slugify(tag_name))
                        post.tags.add(tag)
                
                self.stdout.write(f'Created post: {post.title}')

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample blog data!')
        )
