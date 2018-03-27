from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
import uuid


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True, default="")
    picture = models.ImageField(upload_to='profile_images', blank=True)
    name = models.CharField(max_length=128, blank=True, default="")
    num_articles = models.IntegerField(default=0)
    slug = models.SlugField()
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=4, blank=True, default="")
    location = models.CharField(max_length=128, blank=True, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    # Override the __unicode__() method to return out something meaningful!
    # Remember if you use Python 2.72x, define __unicode__ too!
    def __str__(self):
        return self.user.username


class Article(models.Model):
    author = models.ForeignKey(UserProfile)
    date_published = models.CharField(max_length=8, unique=False)
    book = models.CharField(max_length=128, unique=False)
    views = models.IntegerField(default=0)
    title = models.CharField(max_length=128, unique=True)
    analysis = models.CharField(max_length=2500, unique=False)
    category = models.CharField(max_length=50)
    slug = models.SlugField()
    img = models.ImageField(upload_to='profile_images', blank=True)
    rating = models.FloatField(max_length=5.0, default=0.0)
    book_author = models.CharField(max_length=128, default="")
    book_published = models.CharField(max_length=128, default="")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Article, self).save(*args, **kwargs)
        if self.views < 0 :
            self.views = self.views * -1
        if self.rating < 0:
            self.rating = 0

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_comment = models.CharField(max_length=1000)
    user = models.ForeignKey(UserProfile)
    rating = models.FloatField(max_length=5.0)
    article = models.ForeignKey(Article)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return str(self.id)


class Snippet(models.Model):
    title = models.ForeignKey(Article)
    snippet_title = models.CharField(max_length=128, default = "")
    page = models.IntegerField()
    passage = models.CharField(max_length=500, unique=False)
    analysis = models.CharField(max_length=1000, unique=False)

    def __str__(self):
        return self.snippet_title


class Category(models.Model):
    name = models.CharField(max_length=50, unique=False)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Favourites(models.Model):
    user = models.ForeignKey(UserProfile)
    fav_list = models.ManyToManyField(Article)

    def __str__(self):
        return self.user


