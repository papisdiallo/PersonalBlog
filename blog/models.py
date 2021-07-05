from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from tinymce import HTMLField

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='media/thumbnail_pics')
    category = models.ManyToManyField(Category, related_name='categories')
    overview = models.TextField()
    content = HTMLField('content')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username}'s comment"
    