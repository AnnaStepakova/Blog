from .models import Category
from django.contrib.auth.models import User


# This allows us to pass all categories into base template without using 'get_context_data' multiple times
# Also this function should be added in settings.py in Templates.options to make everything work
def subject_renderer(request):
    return {
        'cat_menu': Category.objects.all(),
    }
