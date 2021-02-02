from django.test import TestCase
from blog.forms import BlogPostForm, UpdateBlogPostForm
from django.contrib.auth.models import User
from blog.models import Category


class AddBlogPostFormTest(TestCase):

    def test_form_with_all_fields_filled(self):
        user = User.objects.create(username='anuta', first_name='Anna', last_name='Grigoreva',
                                        password='okt1267345')
        category = Category.objects.create(name='cat')
        form_data = {'author': user, 'category': category, 'tag': 'some tag', 'title': 'title', 'snippet': 'snippet',
                     'text': 'text'}
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_text_field(self):
        user = User.objects.create(username='anuta', first_name='Anna', last_name='Grigoreva',
                                        password='okt1267345')
        category = Category.objects.create(name='cat')
        form_data = {'author': user, 'category': category, 'tag': 'some tag', 'title': 'title', 'snippet': 'snippet'}
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_category_field(self):
        user = User.objects.create(username='anuta', first_name='Anna', last_name='Grigoreva',
                                        password='okt1267345')
        form_data = {'author': user, 'tag': 'some tag', 'title': 'title', 'snippet': 'snippet', 'text': 'text'}
        form = BlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_tag_field(self):
        user = User.objects.create(username='anuta', first_name='Anna', last_name='Grigoreva',
                                        password='okt1267345')
        category = Category.objects.create(name='cat')
        form_data = {'author': user, 'category': category, 'title': 'title', 'snippet': 'snippet', 'text': 'text'}
        form = BlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_title_field(self):
        user = User.objects.create(username='anuta', first_name='Anna', last_name='Grigoreva',
                                        password='okt1267345')
        category = Category.objects.create(name='cat')
        form_data = {'author': user, 'category': category, 'tag': 'some tag', 'snippet': 'snippet', 'text': 'text'}
        form = BlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_snippet_field(self):
        user = User.objects.create(username='anuta', first_name='Anna', last_name='Grigoreva',
                                        password='okt1267345')
        category = Category.objects.create(name='cat')
        form_data = {'author': user, 'category': category, 'tag': 'some tag', 'title': 'title', 'text': 'text'}
        form = BlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())


class UpdateBlogPostFormTest(TestCase):
    def test_form_with_all_fields_filled(self):
        category = Category.objects.create(name='cat')
        form_data = {'category': category, 'tag': 'new tag', 'title': 'new title', 'snippet': 'new snippet',
                     'text': 'new text'}
        form = UpdateBlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_text_field_filled(self):
        category = Category.objects.create(name='cat')
        form_data = {'category': category, 'tag': 'new tag','title': 'new title', 'snippet': 'new snippet'}
        form = UpdateBlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_category_field_filled(self):
        category = Category.objects.create(name='cat')
        form_data = {'tag': 'new tag', 'title': 'new title', 'snippet': 'new snippet',
                     'text': 'new text'}
        form = UpdateBlogPostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_tag_field_filled(self):
        category = Category.objects.create(name='cat')
        form_data = {'category': category, 'title': 'new title', 'snippet': 'new snippet',
                     'text': 'new text'}
        form = UpdateBlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_title_field_filled(self):
        category = Category.objects.create(name='cat')
        form_data = {'category': category, 'tag': 'new tag', 'snippet': 'new snippet',
                     'text': 'new text'}
        form = UpdateBlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_snippet_field_filled(self):
        category = Category.objects.create(name='cat')
        form_data = {'category': category, 'tag': 'new tag', 'title': 'new title',
                     'text': 'new text'}
        form = UpdateBlogPostForm(data=form_data)
        self.assertFalse(form.is_valid())