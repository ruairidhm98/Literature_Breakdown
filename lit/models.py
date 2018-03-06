from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


class Member(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=15)
    num_articles = models.IntegerField(default=0)
    name = models.CharField(max_length=128, unique=False)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='profile_images', blank=True)
    slug = models.SlugField()

    def __str__(self):
        return self.username


class Article(models.Model):
    author = models.ForeignKey(Member)
    date_published = models.CharField(max_length=8, unique=False)
    book = models.CharField(max_length=128, unique=False)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_comment = models.CharField(max_length=128, unique=False)
    user = models.ForeignKey(Member)
    rating = models.FloatField(max_length=5.0)

    def __str__(self):
        return self.user_comment


class Snippet(models.Model):
    title = models.ForeignKey(Article)
    page = models.IntegerField()
    passage = models.CharField(max_length=300, unique=False)
    analysis = models.CharField(max_length=400, unique=False)

    def __str__(self):
        return self.analysis
