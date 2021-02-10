from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from blog.models import UserProfile
from django.contrib.auth.models import User


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.profile = UserProfile.objects.create(user=self.user, bio='biobio')
        self.profile.save()
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_profile_view(self):
        self.assertTrue(self.logged_in)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_profile_view_context(self):
        self.assertTrue(self.logged_in)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertContains(response, "No posts available")
        self.assertQuerysetEqual(response.context['post_list'], [])
        self.assertEqual(response.context['userprofile'], self.profile)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.profile = UserProfile.objects.create(user=self.user, bio='biobio')
        self.profile.save()
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_update_profile(self):
        self.assertTrue(self.logged_in)
        data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                'twitter_link': 'tw_link', 'website_link': 'w_link'}
        response = self.client.post(reverse('users:edit_profile', kwargs={'pk': self.profile.pk}),
                                    data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserProfile.objects.all().count(), 1)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'bio')

    def test_update_profile(self):
        self.assertTrue(self.logged_in)
        data = {'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                'twitter_link': 'tw_link', 'website_link': 'w_link'}
        response = self.client.post(reverse('users:edit_profile', kwargs={'pk': self.profile.pk}),
                                    data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertEqual(UserProfile.objects.all().count(), 1)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'bio')

    def test_update_profile_no_data(self):
        self.assertTrue(self.logged_in)
        data = {}
        response = self.client.post(reverse('users:edit_profile', kwargs={'pk': self.profile.pk}),
                                    data, follow=False, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile_page.html')
        self.assertEqual(UserProfile.objects.all().count(), 1)


class CreateProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_add_profile(self):
        self.assertTrue(self.logged_in)
        data = {'user': self.user, 'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                'twitter_link': 'tw_link', 'website_link': 'w_link'}
        response = self.client.post(reverse('users:create_profile'), data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserProfile.objects.all().count(), 1)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'bio')
        self.assertEqual(profile.user, self.user)

    def test_add_profile_result(self):
        self.assertTrue(self.logged_in)
        data = {'user': self.user, 'bio': 'bio', 'instagram_link': 'insta_link', 'facebook_link': 'facebook_link',
                'twitter_link': 'tw_link', 'website_link': 'w_link'}
        response = self.client.post(reverse('users:create_profile'), data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertEqual(UserProfile.objects.all().count(), 1)
        profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(profile.bio, 'bio')
        self.assertEqual(profile.user, self.user)

    def test_add_no_profile(self):
        self.assertTrue(self.logged_in)
        data = {}
        response = self.client.post(reverse('users:create_profile'), data, follow=False, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create_profile.html')
        self.assertEqual(UserProfile.objects.all().count(), 0)


class UserRegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sign_up_view(self):
        data = {'username': 'bob', 'first_name': 'Bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                'password1': 'okt1234578', 'password2': 'okt1234578'}
        response = self.client.post(reverse('users:register'), data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(username='bob')
        self.assertEqual(user.first_name, 'Bob')
        self.assertEqual(user.last_name, 'Adams')

    def test_sign_up_view_result(self):
        data = {'username': 'bob', 'first_name': 'Bob', 'last_name': 'Adams', 'email': 'bob@bob.com',
                'password1': 'okt1234578', 'password2': 'okt1234578'}
        response = self.client.post(reverse('users:register'), data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(username='bob')
        self.assertEqual(user.first_name, 'Bob')
        self.assertEqual(user.last_name, 'Adams')

    def test_sign_up_view_no_data(self):
        data = {}
        response = self.client.post(reverse('users:register'), data, follow=False, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertTemplateUsed(response, 'registration/register.html')


class UserEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', email='bob@bob.com')
        self.user.set_password('okt1267345')
        self.user.save()
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_edit_settings(self):
        self.assertTrue(self.logged_in)
        data = {'username': 'bob2', 'first_name': 'Bob2', 'last_name': 'Green', 'email': 'bob2@bob.com'}
        response = self.client.post(reverse('users:edit'), data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'bob2')

    def test_edit_settings_result(self):
        self.assertTrue(self.logged_in)
        data = {'username': 'bob2', 'first_name': 'Bob2', 'last_name': 'Green', 'email': 'bob2@bob.com'}
        response = self.client.post(reverse('users:edit'), data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(id=1)
        self.assertEqual(user.username, 'bob2')


class PasswordUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams', email='bob@bob.com')
        self.user.set_password('okt1267345')
        self.user.save()
        self.logged_in = self.client.login(username='BoB', password='okt1267345')

    def test_password_update_view_success(self):
        self.assertTrue(self.logged_in)
        data = {'old_password': 'okt1267345', 'new_password1': 'yu6784efg', 'new_password2': 'yu6784efg'}
        response = self.client.post(reverse('users:password_change'), data, follow=False, secure=True)
        self.assertEqual(response.status_code, 302)

    def test_password_update_view_failure(self):
        self.assertTrue(self.logged_in)
        data = {'old_password': 'okt1267345'}
        response = self.client.post(reverse('users:password_change'), data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_change.html')

    def test_password_update_view_result(self):
        self.assertTrue(self.logged_in)
        data = {'old_password': 'okt1267345', 'new_password1': 'yu6784efg', 'new_password2': 'yu6784efg'}
        response = self.client.post(reverse('users:password_change'), data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_success.html')


class PasswordSuccessTest(TestCase):
    def test_password_success_page(self):
        response = self.client.get(reverse('users:pass_succ'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/password_success.html')

