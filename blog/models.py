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
    # it should be a foreign key!! or not...
    # category_link = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=150, default="uncategorized")

    def __str__(self):
        if self.likes == 0:
            return f"{self.pub_date}: {self.title} - Not Liked"
        else:
            return f"{self.pub_date}: {self.title} - Liked"

    def get_absolute_url(self):
        return reverse('blog:index')
        # return reverse('blog:detail', args=(str(self.id),))

    # def if_liked_by_user(self, user_id):
    #     if self.likes.filter(id=user_id).exists():
    #         return True
    #     else:
    #         return False


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



