from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # /blog/
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SortTagView.as_view(), name='search_by_tag'),
    path('addpost/', views.AddPostView.as_view(), name='add_post'),
    path('addcategory/', views.AddCategoryView.as_view(), name='add_category'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    path('<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('<int:pk>/delete_comment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('liked/<int:post_id>/', views.like, name='like_post'),
    path('category/<str:cat>', views.category_view, name='category'),
    path('category/', views.CategoryAllView.as_view(), name='category_all'),
]