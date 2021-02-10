from django.contrib import messages
from .models import BlogPost, Category, Comment
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BlogPostForm, UpdateBlogPostForm, AddCategoryForm, CommentForm
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
        comments_connected = Comment.objects.filter(
            blogpost=self.get_object()).order_by('-date_posted')
        data['comments'] = comments_connected
        if self.request.user.is_authenticated:
            data['comment_form'] = CommentForm(instance=self.request.user)
        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(blogpost=self.get_object(), author=self.request.user, body=request.POST.get('body'))
        new_comment.save()
        return HttpResponseRedirect(reverse('blog:detail', args=[str(self.get_object().pk)]))


class AddPostView(generic.CreateView):
    form_class = BlogPostForm
    template_name = 'blog/add_blogpost.html'


class AddCategoryView(generic.CreateView):
    template_name = 'blog/add_category.html'
    form_class = AddCategoryForm


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
        return BlogPost.objects.filter(Q(tag__contains=query) | Q(title__contains=query) | Q(author__username=query))

    def get_context_data(self, **kwargs):  # allows to pass additional params to the template
        data = super().get_context_data(**kwargs)
        data['tag'] = self.request.GET.get('tag')
        return data


def like(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True
    post.save()
    return HttpResponseRedirect(reverse('blog:detail', args=[str(post_id)]))


def delete_comment(request, pk, ck):
    comment = get_object_or_404(Comment, id=request.POST.get('comment_id'))
    pkey = comment.blogpost.id
    try:
        comment.delete()
        messages.success(request, 'You successfully deleted the comment')
    except:
        messages.warning(request, 'The comment could not be deleted.')
    return HttpResponseRedirect(reverse('blog:detail', args=[str(pkey)]))