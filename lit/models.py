from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Member(models.Model):
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=15)
    num_articles = models.IntegerField(default=0)
    name = models.CharField(max_length=128, unique=False)
    email = models.EmailField()
    profile_pic = models.ImageField(upload_to='user_pictures', blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(Member, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Article(models.Model):
    author = models.ForeignKey(Member)
    date_published = models.CharField(max_length=8, unique=False)
    book = models.CharField(max_length=128, unique=False)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=128)
    analysis = models.CharField(max_length=2500, unique=False)
    category = models.CharField(max_length=50)
    slug = models.SlugField()
    img = models.ImageField(upload_to='profile_images', blank=True)
    rating = models.FloatField(max_length=5.0, default=0.0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_comment = models.CharField(max_length=128, unique=False)
    user = models.ForeignKey(Member)
    rating = models.FloatField(max_length=5.0)
    article = models.ForeignKey(Article)

    def __str__(self):
        return self.user_comment


class Snippet(models.Model):
    title = models.ForeignKey(Article)
    page = models.IntegerField()
    passage = models.CharField(max_length=500, unique=False)
    analysis = models.CharField(max_length=1000, unique=False)

    def __str__(self):
        return self.analysis


class Category(models.Model):
    name = models.CharField(max_length=50, unique=False)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.72x, define __unicode__ too!
    def __str__(self):
        return self.user.username
