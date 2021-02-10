from django.test import TestCase
from users.forms import ProfilePageCreateForm, EditProfilePageForm, SignUpForm, EditProfileForm, PasswordUpdateForm
from django.contrib.auth.models import User


class SignUpFormTest(TestCase):
    def test_form_with_all_fields_filled(self):
        form_data = {'username': 'bob', 'first_name': 'Bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                     'password1': 'okt1234578', 'password2': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_username_field(self):
        form_data = {'first_name': 'Bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                     'password1': 'okt1234578', 'password2': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_first_name_field(self):
        form_data = {'username': 'bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                     'password1': 'okt1234578', 'password2': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_last_name_field(self):
        form_data = {'username': 'bob', 'first_name': 'Bob', 'email': 'bob@bob.com',
                     'password1': 'okt1234578', 'password2': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_email_field(self):
        form_data = {'username': 'bob', 'first_name': 'Bob', 'last_name': 'Adams',
                     'password1': 'okt1234578', 'password2': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_password1_field(self):
        form_data = {'username': 'bob', 'first_name': 'Bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                     'password2': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_password2_field(self):
        form_data = {'username': 'bob', 'first_name': 'Bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                     'password1': 'okt1234578'}
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())


class EditProfileFormTest(TestCase):
    def test_form_with_all_fields_filled(self):
        form_data = {'username': 'bob2', 'first_name': 'Bob2', 'last_name': 'Green', 'email': 'bob2@bob.com'}
        form = EditProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_with_empty_username_field(self):
        form_data = {'first_name': 'Bob2', 'last_name': 'Green', 'email': 'bob2@bob.com'}
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_first_name_field(self):
        form_data = {'username': 'bob2', 'last_name': 'Green', 'email': 'bob2@bob.com'}
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_last_name_field(self):
        form_data = {'username': 'bob2', 'first_name': 'Bob2', 'email': 'bob2@bob.com'}
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_with_empty_last_name_field(self):
        form_data = {'username': 'bob2', 'first_name': 'Bob2', 'last_name': 'Green'}
        form = EditProfileForm(data=form_data)
        self.assertFalse(form.is_valid())


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


class PasswordUpdateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', email='bob@bob.com')
        self.user.set_password('okt1267345')
        self.user.save()
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_password_update(self):
        self.assertTrue(self.logged_in)
        form_data = {'old_password': 'okt1267345', 'new_password1': 'yu6784efg', 'new_password2': 'yu6784efg'}
        form = PasswordUpdateForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())

    def test_password_update_empty_old_password_field(self):
        self.assertTrue(self.logged_in)
        form_data = {'new_password1': 'yu6784efg', 'new_password2': 'yu6784efg'}
        form = PasswordUpdateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_password_update_empty_password1_field(self):
        self.assertTrue(self.logged_in)
        form_data = {'old_password': 'okt1267345', 'new_password2': 'yu6784efg'}
        form = PasswordUpdateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_password_update_empty_password2_field(self):
        self.assertTrue(self.logged_in)
        form_data = {'old_password': 'okt1267345', 'new_password1': 'yu6784efg'}
        form = PasswordUpdateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

    def test_password_update_empty_form(self):
        self.assertTrue(self.logged_in)
        form_data = {}
        form = PasswordUpdateForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())

