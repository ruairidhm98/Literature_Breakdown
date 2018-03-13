from django.contrib import admin
from lit.models import Article, Comment, Snippet, Category, UserProfile
from lit.models import *

# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Snippet)
admin.site.register(Category)
admin.site.register(UserProfile)

