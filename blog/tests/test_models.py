from django.test import TestCase
from blog.models import BlogPost, Category, UserProfile, Comment
from django.contrib.auth.models import User


class CategoryTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='cats')

    def test_name_label(self):
        cat = Category.objects.get(id=self.category.id)
        field_label = cat._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        cat = Category.objects.get(id=self.category.id)
        max_length = cat._meta.get_field('name').max_length
        self.assertEquals(max_length, 150)

    def test_get_absolute_url(self):
        cat = Category.objects.get(id=self.category.id)
        self.assertEquals(cat.get_absolute_url(), '/blog/')

    def test_str(self):
        cat = Category.objects.get(id=self.category.id)
        expected = cat.name
        self.assertEquals(expected, str(cat))


class BlogPostTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt1267345')
        self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
                                            tag='testing', category=self.category)

    def test_author_label(self):
        post = BlogPost.objects.get(id=self.post.id)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_title_label(self):
        post = BlogPost.objects.get(id=self.post.id)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_snippet_label(self):
        post = BlogPost.objects.get(id=self.post.id)
        field_label = post._meta.get_field('snippet').verbose_name
        self.assertEquals(field_label, 'snippet')

    def test_text_label(self):
        post = BlogPost.objects.get(id=self.post.id)
        field_label = post._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'text')

    def test_tag_label(self):
        post = BlogPost.objects.get(id=self.post.id)
        field_label = post._meta.get_field('tag').verbose_name
        self.assertEquals(field_label, 'tag')

    def test_category_label(self):
        post = BlogPost.objects.get(id=self.post.id)
        field_label = post._meta.get_field('category').verbose_name
        self.assertEquals(field_label, 'category')

    def test_title_max_length(self):
        post = BlogPost.objects.get(id=self.post.id)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_snippet_max_length(self):
        post = BlogPost.objects.get(id=self.post.id)
        max_length = post._meta.get_field('snippet').max_length
        self.assertEquals(max_length, 250)

    def test_tag_max_length(self):
        post = BlogPost.objects.get(id=self.post.id)
        max_length = post._meta.get_field('tag').max_length
        self.assertEquals(max_length, 150)

    def test_get_absolute_url(self):
        post = BlogPost.objects.get(id=self.post.id)
        self.assertEquals(post.get_absolute_url(), '/blog/')

    def test_str(self):
        post = BlogPost.objects.get(id=self.post.id)
        expected = f"{post.author.username}: {post.title}"
        self.assertEquals(expected, str(post))


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt11102012')
        self.profile = self.user.userprofile

    def test_user_label(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_bio_label(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        field_label = profile._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')

    def test_instagram_link_label(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        field_label = profile._meta.get_field('instagram_link').verbose_name
        self.assertEquals(field_label, 'instagram link')

    def test_facebook_link_label(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        field_label = profile._meta.get_field('facebook_link').verbose_name
        self.assertEquals(field_label, 'facebook link')

    def test_twitter_link_label(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        field_label = profile._meta.get_field('twitter_link').verbose_name
        self.assertEquals(field_label, 'twitter link')

    def test_website_link_label(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        field_label = profile._meta.get_field('website_link').verbose_name
        self.assertEquals(field_label, 'website link')

    def test_bio_length(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        max_length = profile._meta.get_field('bio').max_length
        self.assertEquals(max_length, 500)

    def test_instagram_link_length(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        max_length = profile._meta.get_field('instagram_link').max_length
        self.assertEquals(max_length, 255)

    def test_facebook_link_length(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        max_length = profile._meta.get_field('facebook_link').max_length
        self.assertEquals(max_length, 255)

    def test_twitter_link_length(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        max_length = profile._meta.get_field('twitter_link').max_length
        self.assertEquals(max_length, 255)

    def test_website_link_length(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        max_length = profile._meta.get_field('website_link').max_length
        self.assertEquals(max_length, 255)

    def test_get_absolute_url(self):
        profile = UserProfile.objects.get(id=self.profile.id)
        self.assertEquals(profile.get_absolute_url(), '/blog/')

    def test_str(self):
        profile = self.user.userprofile
        expected = f"{profile.user.username}|{profile.bio}"
        self.assertEquals(expected, str(profile))


class CommentTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt1267345')
        self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
                                        tag='testing', category=self.category)
        self.comment = Comment(blogpost=self.post, author=self.user, body='my comment')
        self.comment.save()
        self.reply = Comment(blogpost=self.post, author=self.user, body='my reply', reply=self.comment)
        self.reply.save()

    def test_author_label(self):
        comm = Comment.objects.get(id=self.comment.id)
        field_label = comm._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_reply_label(self):
        comm = Comment.objects.get(id=self.comment.id)
        field_label = comm._meta.get_field('reply').verbose_name
        self.assertEquals(field_label, 'reply')

        comm = Comment.objects.get(id=self.reply.id)
        field_label = comm._meta.get_field('reply').verbose_name
        self.assertEquals(field_label, 'reply')

    def test_blogpost_label(self):
        comm = Comment.objects.get(id=self.comment.id)
        field_label = comm._meta.get_field('blogpost').verbose_name
        self.assertEquals(field_label, 'blogpost')

    def test_body_label(self):
        comm = Comment.objects.get(id=self.comment.id)
        field_label = comm._meta.get_field('body').verbose_name
        self.assertEquals(field_label, 'body')

    def test_body_length(self):
        comm = Comment.objects.get(id=self.comment.id)
        max_length = comm._meta.get_field('body').max_length
        self.assertEquals(max_length, 500)

        comm = Comment.objects.get(id=self.reply.id)
        max_length = comm._meta.get_field('body').max_length
        self.assertEquals(max_length, 500)

    def test_str(self):
        comm = Comment.objects.get(id=self.comment.id)
        expected = f"{self.comment.author.username}|{self.comment.blogpost.title}|{self.comment.body}"
        self.assertEquals(expected, str(comm))
