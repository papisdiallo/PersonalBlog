from django.urls import path
from Api import views as api_views

urlpatterns = [
    path("posts/", api_views.PostListView.as_view(), name="list-posts-api"),
    path(
        "categories/", api_views.CategoryListView.as_view(), name="list-categories-api"
    ),
]
