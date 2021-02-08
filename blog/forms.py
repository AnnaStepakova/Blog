from django import forms
from .models import BlogPost, Category, Comment


class BlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects, to_field_name="name",
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = BlogPost
        fields = ['author', 'category', 'tag', 'title', 'header_img', 'snippet', 'text']

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'value': '', 'id': 'member', 'type': 'hidden'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UpdateBlogPostForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects, to_field_name="name",
                                      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = BlogPost
        fields = ['category', 'tag', 'title', 'snippet', 'text']

        widgets = {
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),  # form-control is a css class
            'snippet': forms.Textarea(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):

    body = forms.CharField(label=False, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Comment
        fields = ['body']
