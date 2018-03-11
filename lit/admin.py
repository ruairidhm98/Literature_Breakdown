from django.contrib import admin
from lit.models import Member, Article, Comment, Snippet, Category
# Register your models here.

admin.site.register(Member)
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Snippet)
admin.site.register(Category)
