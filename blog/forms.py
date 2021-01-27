from django import forms
from .models import BlogPost, Category

choices = Category.objects.all().values_list('name', 'name')    # a specific format for choices
choice_list = []
for item in choices:
    choice_list.append(item)


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['author', 'category', 'tag', 'title', 'header_img', 'snippet', 'text']

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'member', 'type': 'hidden'}),
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['category', 'tag', 'title', 'snippet', 'text']

        widgets = {
            'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }