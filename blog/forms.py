from django import forms
from .models import BlogPost, Category


def get_choise_list():
    return [item for item in Category.objects.all().values_list('name', 'name')]


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['author', 'category', 'tag', 'title', 'header_img', 'snippet', 'text']

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'member', 'type': 'hidden'}),
            'category': forms.Select(choices=get_choise_list(), attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

        # def __init__(self):
        #     self.model = BlogPost
        #     self.fields = ['author', 'category', 'tag', 'title', 'header_img', 'snippet', 'text']
        #
        #     self.widgets = {
        #         'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'member', 'type': 'hidden'}),
        #         'category': forms.Select(choices=get_choise_list(), attrs={'class': 'form-control'}),
        #         'tag': forms.TextInput(attrs={'class': 'form-control'}),
        #         'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
        #         'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        #         'text': forms.Textarea(attrs={'class': 'form-control'}),
        #     }


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['category', 'tag', 'title', 'snippet', 'text']

        widgets = {
            'category': forms.Select(choices=get_choise_list(), attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }

        # def __init__(self):
        #     self.model = BlogPost
        #     self.fields = ['category', 'tag', 'title', 'snippet', 'text']
        #
        #     self.widgets = {
        #         'category': forms.Select(choices=get_choise_list(), attrs={'class': 'form-control'}),
        #         'tag': forms.TextInput(attrs={'class': 'form-control'}),
        #         'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
        #         'snippet': forms.Textarea(attrs={'class': 'form-control'}),
        #         'text': forms.Textarea(attrs={'class': 'form-control'}),
        #     }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }

        # def __init__(self):
        #     self.model = Category
        #     self.fields = ['name']
        #
        #     self.widgets = {
        #         'name': forms.TextInput(attrs={'class': 'form-control'})
        #     }
