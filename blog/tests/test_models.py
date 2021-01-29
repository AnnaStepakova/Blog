from django.test import TestCase
from blog.models import BlogPost, Category, UserProfile
from django.contrib.auth.models import User


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='cats')

    def test_name_label(self):
        cat = Category.objects.get(id=1)
        field_label = cat._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        cat = Category.objects.get(id=1)
        max_length = cat._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_get_absolute_url(self):
        cat = Category.objects.get(id=1)
        self.assertEquals(cat.get_absolute_url(), '/blog/')

    def test_str(self):
        cat = Category.objects.get(id=1)
        expected = cat.name
        self.assertEquals(expected, str(cat))


class BlogPostTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt11102012')
        self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest', tag='testing', category=self.category)

    def test_author_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_title_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_snippet_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('snippet').verbose_name
        self.assertEquals(field_label, 'snippet')

    def test_text_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_tag_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('tag').verbose_name
        self.assertEquals(field_label, 'tag')

    def test_category_label(self):
        post = BlogPost.objects.get(id=1)
        field_label = post._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'category')

    def test_title_max_length(self):
        post = BlogPost.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_snippet_max_length(self):
        post = BlogPost.objects.get(id=1)
        max_length = post._meta.get_field('snippet').max_length
        self.assertEquals(max_length, 250)

    def test_tag_max_length(self):
        post = BlogPost.objects.get(id=1)
        max_length = post._meta.get_field('tag').max_length
        self.assertEquals(max_length, 150)

    def test_get_absolute_url(self):
        post = BlogPost.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/blog/')

    def test_str(self):
        post = BlogPost.objects.get(id=1)
        expected = f"{post.author.username}: {post.title}"
        self.assertEquals(expected, str(post))


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt11102012')
        self.profile = UserProfile.objects.create(user=self.user, bio='Bio', instagram_link='instagram.com/anutka_st99',
                                                  facebook_link='link1', twitter_link='link2', website_link='link3')

    def test_user_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_bio_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')

    def test_instagram_link_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('instagram_link').verbose_name
        self.assertEquals(field_label, 'instagram link')

    def test_facebook_link_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('facebook_link').verbose_name
        self.assertEquals(field_label, 'facebook link')

    def test_twitter_link_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('twitter_link').verbose_name
        self.assertEquals(field_label, 'twitter link')

    def test_website_link_label(self):
        profile = UserProfile.objects.get(id=1)
        field_label = profile._meta.get_field('website_link').verbose_name
        self.assertEquals(field_label, 'website link')

    def test_bio_length(self):
        profile = UserProfile.objects.get(id=1)
        max_length = profile._meta.get_field('bio').max_length
        self.assertEquals(max_length, 500)

    def test_instagram_link_length(self):
        profile = UserProfile.objects.get(id=1)
        max_length = profile._meta.get_field('instagram_link').max_length
        self.assertEquals(max_length, 255)

    def test_facebook_link_length(self):
        profile = UserProfile.objects.get(id=1)
        max_length = profile._meta.get_field('facebook_link').max_length
        self.assertEquals(max_length, 255)

    def test_twitter_link_length(self):
        profile = UserProfile.objects.get(id=1)
        max_length = profile._meta.get_field('twitter_link').max_length
        self.assertEquals(max_length, 255)

    def test_website_link_length(self):
        profile = UserProfile.objects.get(id=1)
        max_length = profile._meta.get_field('website_link').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        profile = UserProfile.objects.get(id=1)
        self.assertEquals(profile.get_absolute_url(), '/blog/')

    def test_str(self):
        profile = UserProfile.objects.get(id=1)
        expected = f"{self.profile.user.username}|{self.profile.bio}"
        self.assertEquals(expected, str(profile))