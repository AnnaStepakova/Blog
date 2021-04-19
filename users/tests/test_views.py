from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from blog.models import UserProfile, BlogPost, Category
from django.contrib.auth.models import User
from users.views import follow


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class ProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.profile = self.user.userprofile
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
        self.assertQuerysetEqual(response.context['object_list'], [])
        self.assertEqual(response.context['userprofile'], self.profile)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class EditProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username='BoB', first_name='Bob', last_name='Adams')
        self.user.set_password('okt1267345')
        self.user.save()
        self.profile = self.user.userprofile
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

    def test_default_profile_creation(self):
        profile = self.user.userprofile
        profile_in_db = UserProfile.objects.get(id=self.user.userprofile.id)
        self.assertEqual(profile, profile_in_db)

    def test_default_profile_fields(self):
        profile = self.user.userprofile
        self.assertEqual(profile.bio, 'I have no bio yet :(')
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.instagram_link, None)
        self.assertEqual(profile.facebook_link, None)
        self.assertEqual(profile.twitter_link, None)
        self.assertEqual(profile.website_link, None)


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
        user = User.objects.get(id=self.user.id)
        self.assertEqual(user.username, 'bob2')

    def test_edit_settings_result(self):
        self.assertTrue(self.logged_in)
        data = {'username': 'bob2', 'first_name': 'Bob2', 'last_name': 'Green', 'email': 'bob2@bob.com'}
        response = self.client.post(reverse('users:edit'), data, follow=True, secure=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/home.html')
        self.assertEqual(User.objects.all().count(), 1)
        user = User.objects.get(id=self.user.id)
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


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class FollowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        self.user1 = User.objects.create(username='BoB1', first_name='Bob', last_name='Adams', email='bob@bob.com')
        self.user1.set_password('okt1267345')
        self.user1.save()
        self.logged_in1 = self.client.login(username='BoB1', password='okt1267345')
        self.profile1 = self.user1.userprofile

        self.user2 = User.objects.create(username='BoB2', first_name='Bob', last_name='Adams', email='bob@bob.com')
        self.user2.set_password('okt12')
        self.user2.save()
        self.logged_in2 = self.client.login(username='BoB2', password='okt12')
        self.profile2 = self.user2.userprofile
        self.category = Category.objects.create(name='cats')
        self.post = BlogPost.objects.create(author=self.user1, title='test', snippet='test post', text='TestTest',
                                            tag='testing', category=self.category)
        self.request = self.factory.post(reverse('users:profile', kwargs={'pk': self.profile1.pk}),
                                         {'userprofile_to_follow_id': self.profile1.pk})
        self.request.user = self.user2
        self.response = follow(self.request, self.profile1.pk)

    def test_follow(self):
        self.assertTrue(self.logged_in1)
        self.assertTrue(self.logged_in2)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.profile1 in self.profile2.subs.all(), True)
        self.assertEqual(self.profile2 in self.profile1.follow.all(), True)

    def test_unfollow(self):
        self.assertTrue(self.logged_in1)
        self.assertTrue(self.logged_in2)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.profile1 in self.profile2.subs.all(), True)
        self.assertEqual(self.profile2 in self.profile1.follow.all(), True)

        request = self.factory.post(reverse('users:profile', kwargs={'pk': self.profile1.pk}),
                                    {'userprofile_to_follow_id': self.profile1.pk})
        request.user = self.user2
        response = follow(request, self.profile1.pk)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.profile1 in self.profile2.subs.all(), False)
        self.assertEqual(self.profile2 in self.profile1.follow.all(), False)

    def test_show_followers(self):
        self.assertTrue(self.logged_in1)
        self.assertTrue(self.logged_in2)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.profile1 in self.profile2.subs.all(), True)
        self.assertEqual(self.profile2 in self.profile1.follow.all(), True)

        response = self.client.get(reverse('users:followers', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/followers.html')
        self.assertContains(response, f"{self.profile2.user.get_username()}")

    def test_show_subs(self):
        self.assertTrue(self.logged_in1)
        self.assertTrue(self.logged_in2)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.profile1 in self.profile2.subs.all(), True)
        self.assertEqual(self.profile2 in self.profile1.follow.all(), True)

        response = self.client.get(reverse('users:subs', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'users/subs.html')
        self.assertContains(response, f"{self.profile1.user.get_username()}")

    def test_show_feed(self):
        self.assertTrue(self.logged_in1)
        self.assertTrue(self.logged_in2)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile1.pk}))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('users:profile', kwargs={'pk': self.profile2.pk}))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.profile1 in self.profile2.subs.all(), True)
        self.assertEqual(self.profile2 in self.profile1.follow.all(), True)

        response = self.client.get(reverse('users:feed', kwargs={'pk': self.profile2.pk}))
        self.assertTemplateUsed(response, 'users/feed.html')
        self.assertContains(response, f"{self.profile1.user.get_username()}")







