from django import forms
from django.contrib.auth.models import User
from lit.models import UserProfile, Article, Comment


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

    categories = [
        ('Fiction', 'Fiction'),
        ('Short Story', 'Short Story'),
        ('Scripture', 'Scripture'),
        ('Philosophy', 'Philosophy')
    ]

    title = forms.CharField(widget=forms.Textarea)
    book = forms.CharField(widget=forms.Textarea)
    book_author = forms.CharField(widget=forms.Textarea)
    book_published = forms.CharField(widget=forms.Textarea)
    analysis = forms.CharField(widget=forms.Textarea)
    category = forms.CharField(widget=forms.Select(choices=categories))

    class Meta:
        model = Article
        fields = ('title', 'book', 'book_author', 'book_published', 'analysis', 'category', 'img')


class CommentForm(forms.ModelForm):
    rating = forms.DecimalField(min_value=0, max_value=5, max_digits=2, decimal_places=1)
    
    class Meta:
        model = Comment
        fields = ('user_comment', 'rating')
