from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from tinymce import HTMLField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Profile(models.Model):
    profile_pic = models.ImageField(upload_to="media/profile_pics")
    profession = models.CharField(max_length=100)



class Post(models.Model):
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to='media/thumbnail_pics')
    category = models.ManyToManyField(Category, related_name='categories')
    overview = models.TextField()
    content = HTMLField('content')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

