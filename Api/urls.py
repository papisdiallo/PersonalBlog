from django.urls import path
from Api import views as api_views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

# Need to add the token verify view later

urlpatterns = [
    path("posts/", api_views.PostListView.as_view(), name="list-posts-api"),
    path("auth/register/", api_views.RegisterApiView.as_view(), name="register-view"),
    path("auth/login/", api_views.LoginApiView.as_view(), name="login-view"),
    path("email-verification/", api_views.EmailVerificationView.as_view(), name="email-verification-view"),
    path("get-started/", api_views.apiDocsView, name="list-posts-api"),
    path(
        "categories/", api_views.CategoryListView.as_view(), name="list-categories-api"
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
