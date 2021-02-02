from .models import BlogPost, Category
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BlogPostForm, UpdateBlogPostForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Count


class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        return BlogPost.objects.all().order_by('-pub_date')


def category_view(request, cat):
    post_list = BlogPost.objects.filter(category__name=cat)
    return render(request, 'blog/category.html', {'post_list': post_list, 'cat': cat})


class DetailView(generic.DetailView):
    model = BlogPost
    template_name = 'blog/detail.html'

    def get_context_data(self, *args, **kwargs):
        data = super(DetailView, self).get_context_data(**kwargs)
        curr_post = get_object_or_404(BlogPost, id=self.kwargs['pk'])
        liked = False
        if curr_post.likes.filter(id=self.request.user.id).exists():
            liked = True
        data['liked'] = liked
        return data


class AddPostView(generic.CreateView):
    form_class = BlogPostForm
    template_name = 'blog/add_blogpost.html'


class AddCategoryView(generic.CreateView):
    model = Category
    template_name = 'blog/add_category.html'
    fields = '__all__'


class CategoryAllView(generic.ListView):
    template_name = 'blog/category_list.html'
    context_object_name = 'cat_list'

    def get_queryset(self):
        return Category.objects.all()

    def get_context_data(self, **kwargs):
        categories = Category.objects.all().annotate(posts_count=Count('blogpost'))
        data = super(CategoryAllView, self).get_context_data(**kwargs)
        data['categories'] = categories
        return data


class UpdatePostView(generic.UpdateView):
    template_name = 'blog/update_blogpost.html'
    model = BlogPost
    form_class = UpdateBlogPostForm


class DeletePostView(generic.DeleteView):
    model = BlogPost
    template_name = 'blog/delete_blogpost.html'
    success_url = reverse_lazy('blog:index')


class SortTagView(generic.ListView):
    model = BlogPost
    template_name = 'blog/sort_tag.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        query = self.request.GET.get('tag')
        return BlogPost.objects.filter(Q(tag__contains=query) | Q(title__contains=query))

    def get_context_data(self, **kwargs):  # allows to pass additional params to the template
        data = super().get_context_data(**kwargs)
        data['tag'] = self.request.GET.get('tag')
        return data


def like(request, post_id):
    post = get_object_or_404(BlogPost, pk=request.POST.get('blogpost_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    post.save()
    return HttpResponseRedirect(reverse('blog:detail', args=[str(post_id)]))



