from django.urls import path
from Api import views as api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Need to add the token verify view later

urlpatterns = [
    path("posts/", api_views.PostListView.as_view(), name="list-posts-api"),
    path("register/", api_views.RegisterApiView.as_view(), name="register-view"),
    path("get-started/", api_views.apiDocsView, name="list-posts-api"),
    path(
        "categories/", api_views.CategoryListView.as_view(), name="list-categories-api"
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
