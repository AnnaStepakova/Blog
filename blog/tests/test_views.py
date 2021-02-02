from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from blog.models import BlogPost, Category, UserProfile
from django.contrib.auth.models import User
# from blog.views import like


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


class BlogpostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='cat')
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', password='okt1267345')
        self.profile = UserProfile.objects.create(user=self.user, bio='biobio')
        self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
                                       tag='testing', category=self.category)
        self.response = self.client.get(reverse('blog:detail', kwargs={'pk': self.post.pk}))

    def test_detail_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')

    def test_post_if_liked(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')
        self.assertIn('liked', self.response.context)

    def test_post_context(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'blog/detail.html')
        self.assertContains(self.response, f"{self.user.first_name} {self.user.last_name}")
        self.assertContains(self.response, f"{self.post.title}")
        self.assertContains(self.response, f"{self.post.text}")
        self.assertContains(self.response, f"{self.post.tag}")


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
        self.user = User.objects.create_user(username='jacob',  password='top_secret')
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

# TODO: write more tests!!!
# class LikeTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.user = User.objects.create_user(username='jacob', password='top_secret')
#         self.category = Category.objects.create(name='cat')
#         self.post = BlogPost.objects.create(author=self.user, title='test', snippet='test post', text='TestTest',
#                                             tag='testing_tag', category=self.category)
#
#     def test_like(self):
#         # url = reverse('blog:like_post', kwargs={'post_id': self.post.id})
#         request = self.client.get('/blog/liked/1', follow=True)
#         request.user = self.user
#         pk = self.post.id
#         response = like(request, pk)
#         self.assertRedirects(response, '/blog/1', status_code=302,
#                              target_status_code=200, fetch_redirect_response=True)
#         # self.assertRedirects(response, reverse('blog:detail', kwargs={'post_id': self.post.id}))
