from django.contrib import admin
from .models import BlogPost, Category, UserProfile

# Register your models here.
admin.site.register(BlogPost)
admin.site.register(Category)
admin.site.register(UserProfile)