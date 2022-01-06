from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from tinymce import HTMLField
from django.template.defaultfilters import slugify

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=50)
    category_slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
            super(Post, self).save(*args, **kwargs)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    thumbnail = models.ImageField(upload_to="media/thumbnail_pics")
    category = models.ManyToManyField(Category, related_name="categories")
    post_slug = models.SlugField(blank=True, null=True)
    overview = models.TextField()
    content = HTMLField("content")
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        return super(Post, self).save(*args, **kwargs)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author.username}'s comment"


class Contact(models.Model):
    message = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} contacted me with the email {self.email}"
