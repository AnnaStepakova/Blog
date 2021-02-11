import datetime
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:index')


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    snippet = models.CharField(max_length=250)
    header_img = models.ImageField(null=True, blank=True, upload_to='images/')
    text = RichTextField(blank=True, null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    liked = models.BooleanField(default=False)
    likes = models.ManyToManyField(User, related_name='blogposts')
    tag = models.CharField(max_length=150, default="No tag")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.author.username}: {self.title}"

    def get_absolute_url(self):
        return reverse('blog:index')


class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    profile_img = models.ImageField(null=True, blank=True, upload_to='images/profile/')
    instagram_link = models.CharField(max_length=255, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    website_link = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.user.get_username() + '|' + self.bio

    def get_absolute_url(self):
        return reverse('blog:index')


class Comment(models.Model):
    blogpost = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        result = self.author.get_username() + '|' + self.blogpost.title + '|' + self.body
        if self.reply:
            result += ' ( reply to: ' + self.reply.author.username + ')'
        return result
