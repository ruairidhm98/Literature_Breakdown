from django import forms
from django.contrib.auth.models import User
from lit.models import UserProfile, Article


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'name', 'picture',)


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'book', 'book_author', 'book_published', 'analysis', 'category', 'img')
