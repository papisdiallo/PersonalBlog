from blog.models import Post, Category
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "category_slug",
        )


class PostSerializer(serializers.ModelSerializer):
    category = CategorySerializer(Category.objects.all(), read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            "author",
            "title",
            "thumbnail",
            "category",
            "overview",
            "content",
            "post_slug",
        )
