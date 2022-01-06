from django.shortcuts import render, reverse, get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from Users.serializers import RegisterSerializer, LoginSerializer
from Api.serializers import PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
import jwt
from drf_yasg import openapi
from blog.models import Post, Category, Comment
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from .permissions import IsAuthor

# from django.views import generics
from blog.models import Post, Category
from .serializers import PostSerializer, CategorySerializer

User = get_user_model()
# class PostListView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response({"data": serializer.data})


class PostListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "post_slug"

    def get(self, request, *args, **kwargs):
        # replace with get_object_or_404
        post = get_object_or_404(Post, post_slug=self.kwargs.get("post_slug"))
        serializer = self.serializer_class(post)
        comments = CommentSerializer(post.comments.all(), many=True)
        return Response({"data": serializer.data, "post_comments": comments.data})


def apiDocsView(request):
    # need to make a new side bar different with the same layout
    context = {}
    return render(request, "Api/api-get-started.html", context)


class RegisterApiView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(
            email=serializer.data["email"]
        )  # getting newly created user
        data = {}
        access_token = RefreshToken.for_user(user).access_token
        domainName = get_current_site(request)
        emailVerificationUrl = reverse("email-verification-view")
        print("this is the path", emailVerificationUrl)
        emailLinkVerification = (
            f"http://{domainName}{emailVerificationUrl}?token={access_token}"
        )

        email_body = f"Hi, {serializer.data['username']}, \n. Please just copy the token below and paste to the verify email endpoint.\n Access_token: {emailLinkVerification}"

        subject = "Email Verification"
        to = serializer.data["email"]
        data["email_body"] = email_body
        data["subject"] = subject
        data["to"] = to
        data["from_email"] = settings.EMAIL_HOST_USER
        # send the email to the newly created user for verification
        Util.send_email(data)
        return Response(
            {
                "message": f"An email has been sent to {serializer.data['email']} for verification",
                "user": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class EmailVerificationView(views.APIView):
    serializer_class = RegisterSerializer
    token_config = openapi.Parameter(
        "token",
        in_=openapi.IN_QUERY,
        description="description for now",
        type=openapi.TYPE_STRING,
    )

    @swagger_auto_schema(manual_parameters=[token_config])
    def get(self, request, *args, **kwargs):
        # get the acess token
        access_token = self.request.GET.get("token")
        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms="HS256"
            )  # decode the acess token
            user = User.objects.get(id=payload["user_id"])  # gettting the encoded user
            user.is_verified = True
            user.save()
        except jwt.ExpiredSignatureError:
            return Response(
                {
                    "Error": "this token has expired! Please get another one with your refresh token"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except jwt.exceptions.DecodeError:
            return Response(
                {"Error": "The provided token is not valid. Please try again..."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # return a new access token and the refresh token of the user it self with the expired date
        return Response(
            {"message": "Email verification completed Successfully!"},
            status=status.HTTP_200_OK,
        )


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class PostCommentsListAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self, *args, **kwargs):
        post = get_object_or_404(Post, post_slug=self.kwargs.get("post_slug"))
        return self.queryset.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, post_slug=self.kwargs.get("post_slug"))
        instance = serializer.save(author=self.request.user, post=post)


class CommentRudAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsAuthor)
    serializer_class = CommentSerializer
    lookup_field = "id"
    queryset = Comment.objects.all()

    # def perform_update(self, serializer):
    #     post = get_object_or_404(Post, post_slug=self.kwargs.get("post_slug"))
    #     instance = serializer.save(author=self.request.user, post=post)
