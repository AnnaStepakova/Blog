from django.test import TestCase
from users.forms import ProfilePageCreateForm, EditProfilePageForm
from django.contrib.auth.models import User


class ProfilePageCreateFormTest(TestCase):
    def test_form_with_all_fields_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = ProfilePageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_bio_field_filled(self):
        form_data = {'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = ProfilePageCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_insta_link_field_filled(self):
        form_data = {'bio': 'bio', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = ProfilePageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_facebook_link_field_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = ProfilePageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_tw_link_field_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'website_link': 'w_link'}
        form = ProfilePageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_website_link_field_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link'}
        form = ProfilePageCreateForm(data=form_data)
        self.assertTrue(form.is_valid())


class ProfilePageUpdateFormTest(TestCase):
    def test_form_with_all_fields_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = EditProfilePageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_bio_field_filled(self):
        form_data = {'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = EditProfilePageForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_insta_link_field_filled(self):
        form_data = {'bio': 'bio', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = EditProfilePageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_facebook_link_field_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link',
                     'twitter_link': 'tw_link', 'website_link': 'w_link'}
        form = EditProfilePageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_tw_link_field_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'website_link': 'w_link'}
        form = EditProfilePageForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_website_link_field_filled(self):
        form_data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                     'twitter_link': 'tw_link'}
        form = EditProfilePageForm(data=form_data)
        self.assertTrue(form.is_valid())


