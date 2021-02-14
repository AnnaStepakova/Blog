from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy, reverse
from blog.models import BlogPost, UserProfile
from .forms import SignUpForm, EditProfileForm, PasswordUpdateForm, EditProfilePageForm, ProfilePageCreateForm
from django.views.generic.list import MultipleObjectMixin
from django.core.paginator import Paginator


class ProfilePageView(generic.DetailView, MultipleObjectMixin):
    model = UserProfile
    template_name = 'users/profile.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        profile = get_object_or_404(UserProfile, id=self.kwargs['pk'])
        object_list = BlogPost.objects.filter(author=profile.user).order_by('-pub_date')
        in_subs = False
        if self.request.user.userprofile.subs.filter(id=profile.id).exists():
            in_subs = True
        data = super(ProfilePageView, self).get_context_data(object_list=object_list, **kwargs)
        data['userprofile'] = profile
        data['in_subs'] = in_subs
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


def follow(request, pk):
    user = request.user
    userprofile = get_object_or_404(UserProfile, id=user.userprofile.id)
    userprofile_to_follow_id = request.POST.get('userprofile_to_follow_id')
    userprofile_to_follow = get_object_or_404(UserProfile, id=userprofile_to_follow_id)
    if userprofile.subs.filter(id=userprofile_to_follow_id).exists():
        userprofile.subs.remove(userprofile_to_follow)
        userprofile_to_follow.follow.remove(userprofile)
    else:
        userprofile.subs.add(userprofile_to_follow)
        userprofile_to_follow.follow.add(userprofile)
    userprofile.save()
    userprofile_to_follow.save()
    return HttpResponseRedirect(reverse('users:profile', args=[str(userprofile_to_follow_id)]))


def show_followers(request, pk):
    profile = get_object_or_404(UserProfile, id=pk)
    followers = profile.follow.get_queryset()
    return render(request, 'users/followers.html', {'followers': followers, 'userprofile': profile})


def show_subs(request, pk):
    profile = get_object_or_404(UserProfile, id=pk)
    subs = profile.subs.get_queryset()
    return render(request, 'users/subs.html', {'subs': subs, 'userprofile': profile})


def show_feed(request, pk):
    profile = get_object_or_404(UserProfile, id=pk)
    subs = profile.subs.get_queryset()
    post_list = []
    for sub in subs:
        post_list += BlogPost.objects.filter(author=sub.user).order_by('-pub_date')

    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request, 'users/feed.html', {'page_obj': page_obj, 'userprofile': profile})
