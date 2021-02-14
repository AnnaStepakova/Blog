from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from blog.models import BlogPost, Category, UserProfile, Comment
from django.contrib.auth.models import User
import json


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        Category.objects.create(name='cat')
        User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt1267345')

    def test_index_view_with_post(self):
        category = Category.objects.get(id=1)
        user = User.objects.get(id=1)
        post = BlogPost.objects.create(author=user, title='test1', snippet='test post1', text='TestTest1',
                                       tag='testing1', category=category)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertQuerysetEqual(response.context['post_list'], map(repr, [post]))

    def test_index_view_no_posts(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertContains(response, "No posts available")
        self.assertQuerysetEqual(response.context['post_list'], [])


class CategoryAllViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cat_view_with_category(self):
        cat = Category.objects.create(name='cat')
        response = self.client.get(reverse('blog:category_all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_list.html')
        self.assertQuerysetEqual(response.context['cat_list'], map(repr, [cat]))
        self.assertIn('categories', response.context)

    def test_cat_view_with_no_categories(self):
        response = self.client.get(reverse('blog:category_all'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category_list.html')
        self.assertQuerysetEqual(response.context['cat_list'], [])
        self.assertContains(response, "No categories available")


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class BlogpostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.profile = UserProfile.objects.create(user=self.user, bio='biobio')
        self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
                                            tag='testing', category=self.category)
        self.comment = Comment.objects.create(blogpost=self.post, author=self.user, body='new comment')
        self.response = self.client.get(reverse('blog:detail', kwargs={'pk': self.post.pk}))

        # f = open("/tmp/index.html", 'wb')
        # f.write(self.response.content)
        # f.close()

    def test_detail_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

    def test_post_if_liked(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')
        self.assertIn('liked', self.response.context)

    def test_post_context_text(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')
        self.assertContains(self.response, f"{self.user.first_name} {self.user.last_name}")
        self.assertContains(self.response, f"{self.post.title}")
        self.assertContains(self.response, f"{self.post.text}")
        self.assertContains(self.response, f"{self.post.tag}")

    def test_context_params(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')
        self.assertEqual(self.response.context['comments'].count(), 1)
        self.assertQuerysetEqual(self.response.context['comments'], map(repr, [self.comment]))
        self.assertEqual(self.response.context['liked'], False)

    def test_context_comment_form(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)

        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

        response = self.client.post('/blog/1/', {'body': 'my new comment'}, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.all().count(), 2)
        comm = Comment.objects.get(id=2)
        self.assertEqual(comm.body, 'my new comment')


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt1267345')

    def test_category_with_no_posts(self):
        response = self.client.get(reverse('blog:category', kwargs={'cat': self.category.name}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category.html')
        self.assertContains(response, "No posts available")
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_category_post_list(self):
        post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
                                       tag='testing', category=self.category)
        response = self.client.get(reverse('blog:category', kwargs={'cat': self.category.name}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/category.html')
        self.assertQuerysetEqual(response.context['post_list'], map(repr, [post]))
        self.assertIn('cat', response.context)


class SortTagViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='jacob', password='top_secret')
        self.category = Category.objects.create(name='cat')
        self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
                                            tag='testing_tag', category=self.category)

    def test_sort_with_no_posts(self):
        response = self.client.get(reverse('blog:search_by_tag'), {'tag': 'my_new_tag'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/sort_tag.html')
        self.assertIn('tag', response.context)
        self.assertContains(response, "No posts available")

    def test_details_sort_tag(self):
        response = self.client.get(reverse('blog:search_by_tag'), {'tag': self.post.tag})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/sort_tag.html')
        self.assertIn('tag', response.context)
        self.assertContains(response, f"{self.post.tag}")

    def test_details_sort_category(self):
        response = self.client.get(reverse('blog:search_by_tag'), {'tag': self.category.name})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/sort_tag.html')
        self.assertIn('tag', response.context)
        self.assertContains(response, f"{self.category.name}")


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AddPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')  # , password='okt1267345')
        self.user.set_password('okt1267345')
        self.user.save()

    def test_add_post(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        data = {
            'author': self.user.id,
            'category': self.category,
            'tag': 'some tag',
            'title': 'new post',
            'snippet': 'snippet',
            'text': 'some text'
        }
        response = self.client.post('/blog/addpost/', data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.all().count(), 1)
        post = BlogPost.objects.get(author=self.user)
        self.assertEqual(post.title, 'new post')

        response2 = self.client.post('/blog/addpost/', data, follow=True, secure=True)
        self.assertEqual(response2.status_code, 200)
        self.assertTemplateUsed(response2, 'blog/index.html')
        self.assertEqual(BlogPost.objects.all().count(), 2)

    def test_add_no_post(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        data = {}
        response = self.client.post('/blog/addpost/', data, follow=False, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/add_blogpost.html')
        self.assertEqual(BlogPost.objects.all().count(), 0)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class UpdatePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.post = BlogPost(author=self.user, category=self.category, tag='some tag', title='new post',
                             snippet='snippet', text='some text')
        self.post.save()

    def test_update_post(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        cat = Category.objects.create(name='new')
        id = self.post.pk
        data = {
            'category': cat,
            'tag': 'new tag',
            'title': 'new title',
            'snippet': 'new snippet',
            'text': 'new text'
        }
        response = self.client.post(f'/blog/{id}/update/', data, follow=False, secure=True)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.all().count(), 1)
        post = BlogPost.objects.get(author=self.user)
        self.assertEqual(post.title, 'new title')

        response = self.client.post(f'/blog/{id}/update/', data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_no_update_post(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        cat = Category.objects.create(name='new')
        id = self.post.pk
        data = {}
        response = self.client.post(f'/blog/{id}/update/', data, follow=False, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/update_blogpost.html')
        self.assertEqual(BlogPost.objects.all().count(), 1)
        post = BlogPost.objects.get(author=self.user)
        self.assertEqual(post.title, 'new post')


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DeletePostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.post = BlogPost(author=self.user, category=self.category, tag='some tag', title='new post',
                             snippet='snippet', text='some text')
        self.post.save()

    def test_delete_post_result(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        id = self.post.pk
        response = self.client.post(f'/blog/{id}/delete/', follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(BlogPost.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'blog/index.html')

    def test_delete_post(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        id = self.post.pk
        response = self.client.post(f'/blog/{id}/delete/', follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(BlogPost.objects.all().count(), 0)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class AddCategoryViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()

    def test_add_category(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        data = {'name': 'cats'}
        response = self.client.post('/blog/addcategory/', data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.all().count(), 1)
        category = Category.objects.get(id=1)
        self.assertEqual(category.name, 'cats')

    def test_add_category_result(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        data = {'name': 'cats'}
        response = self.client.post('/blog/addcategory/', data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertEqual(Category.objects.all().count(), 1)
        category = Category.objects.get(id=1)
        self.assertEqual(category.name, 'cats')

    def test_add_no_category(self):
        logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(logged_in)
        data = {}
        response = self.client.post('/blog/addcategory/', data, follow=False, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/add_category.html')
        self.assertEqual(BlogPost.objects.all().count(), 0)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class DeleteCommentTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.post = BlogPost(author=self.user, category=self.category, tag='some tag', title='new post',
                             snippet='snippet', text='some text')
        self.post.save()
        self.comment = Comment.objects.create(blogpost=self.post, author=self.user, body='new comment')
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_delete_comment(self):
        self.assertTrue(self.logged_in)
        response = self.client.get(reverse('blog:detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(Comment.objects.all().count(), 1)

        response = self.client.post(reverse('blog:delete_comment', kwargs={'pk': self.post.pk, 'ck': self.comment.pk}),
                                    data={'comment_id': self.comment.pk}, follow=False)

        f = open("/tmp/index.html", 'wb')
        f.write(response.content)
        f.close()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.all().count(), 0)

    def test_delete_comment_check_result_page(self):
        self.assertTrue(self.logged_in)
        response = self.client.get(reverse('blog:detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')

        response = self.client.post(reverse('blog:delete_comment', kwargs={'pk': self.post.pk, 'ck': self.comment.pk}),
                                    data={'comment_id': self.comment.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(Comment.objects.all().count(), 0)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class LikeTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.post = BlogPost(author=self.user, category=self.category, tag='some tag', title='new post',
                             snippet='snippet', text='some text')
        self.post.save()
        self.comment = Comment.objects.create(blogpost=self.post, author=self.user, body='new comment')
        self.logged_in = self.client.login(username='BoB', password='okt1267345')
        self.assertTrue(self.logged_in)
        self.response = self.client.get(reverse('blog:detail', kwargs={'pk': self.post.pk}))

    def test_like(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

        response = self.client.post('/blog/liked/1/', data={'post_id': self.post.pk}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.likes.count(), 1)

    def test_like_result_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

        response = self.client.post('/blog/liked/1/', data={'post_id': self.post.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(self.post.likes.count(), 1)

    def test_unlike(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

        response = self.client.post('/blog/liked/1/', data={'post_id': self.post.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(self.post.likes.count(), 1)

        response = self.client.post('/blog/liked/1/', data={'post_id': self.post.pk}, follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.post.likes.count(), 0)

    def test_unlike_result_page(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

        response = self.client.post('/blog/liked/1/', data={'post_id': self.post.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(self.post.likes.count(), 1)

        response = self.client.post('/blog/liked/1/', data={'post_id': self.post.pk}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/detail.html')
        self.assertEqual(self.post.likes.count(), 0)
