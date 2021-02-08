from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from blog.models import UserProfile, BlogPost
from .forms import SignUpForm, EditProfileForm, PasswordUpdateForm, EditProfilePageForm, ProfilePageCreateForm
from . import views


class ProfilePageView(generic.DetailView):
    model = UserProfile
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        data = super(ProfilePageView, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, id=self.kwargs['pk'])
        data['userprofile'] = profile
        posts = BlogPost.objects.filter(author=self.request.user)
        data['post_list'] = posts
        return data


class EditProfilePageView(generic.UpdateView):
    form_class = EditProfilePageForm
    template_name = 'users/edit_profile_page.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user.userprofile


class CreateProfilePageView(generic.CreateView):
    model = UserProfile
    template_name = 'users/create_profile.html'
    form_class = ProfilePageCreateForm

    # making user.id available to the profile so we can associate
    # user with their profile page
    def form_valid(self, form):
        form.instance.user = self.request.user  # grab the user filling the form
        return super().form_valid(form)


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('home:home')        # reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user


class PasswordUpdateView(PasswordChangeView):
    form_class = PasswordUpdateForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('users:pass_succ')


def password_success(request):
    return render(request, 'users/password_success.html', {})