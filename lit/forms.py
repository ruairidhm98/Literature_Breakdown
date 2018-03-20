from django import forms
from django.contrib.auth.models import User
from lit.models import UserProfile, Article, Comment, Snippet


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.Textarea)
    email = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    website = forms.CharField(widget=forms.Textarea)
    name = forms.CharField(widget=forms.Textarea)
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
    user_comment = forms.CharField(widget=forms.Textarea)
    rating = forms.DecimalField(min_value=0, max_value=5, max_digits=2, decimal_places=1)
    
    class Meta:
        model = Comment
        fields = ('user_comment', 'rating')


class SnippetForm(forms.ModelForm):
   snippet_title = forms.CharField(widget=forms.Textarea)
   page = forms.CharField(widget=forms.Textarea)
   passage = forms.CharField(widget=forms.Textarea)
   analysis = forms.CharField(widget=forms.Textarea)

   class Meta:
       model = Snippet
       fields = ('snippet_title', 'page', 'passage', 'analysis')

