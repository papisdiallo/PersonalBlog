from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from Users.serializers import RegisterSerializer
from django.contrib.auth import get_user_model

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


class PostListView(APIView):
    permission_classes = (IsAuthenticated,)
    #  permission_classes = [HasAPIKey] authenticated using the apikey
    # Need to add the post link url by using the hyperLinkRelatedField to the serialzer


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

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(generics.GenericAPIView):
    # need to call the serializer and do
    # all the rest in the login serializer and like
    # validating the data and generating a token
    pass
