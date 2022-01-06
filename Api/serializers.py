from blog.models import Post, Category, Comment
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "name",
            "category_slug",
        )


class PostSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(Category.objects.all(), read_only=True, many=True)
    category_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "author",
            "category_count",
            "comments_count",
            "title",
            "thumbnail",
            "overview",
            "post_slug",
            "date_posted",
        )

    def get_category_count(self, obj):
        return obj.category.all().count()

    def get_comments_count(self, obj):
        return obj.category.all().count()


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "author",
            "post",
            "content",
            "date_commented",
        )

    def get_post(self, obj):
        return {
            "title": obj.post.title,
            "author": obj.post.author.username,
            "post slug": obj.post.post_slug,
        }

    def get_author(self, obj):
        return obj.author.username
