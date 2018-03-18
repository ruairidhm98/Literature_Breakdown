from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django import forms
from lit.models import *
from lit.forms import *
from datetime import datetime
from lit.webhose_search import run_query


def index(request):
    article_list_trending = Article.objects.order_by('-rating')[:5]
    article_list_new = Article.objects.order_by('date_published')[:5]
    category_list = Category.objects.all()
    
    context_dict = {'articles_new': article_list_new,
                    'articles_trending' : article_list_trending,
                    'categories': category_list}
    return render(request, 'lit/index.html', context=context_dict)


def search(request):

    result_list = []
    context_dict = {}

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            articles = Article.objects.filter()
            for article in articles:
                if query.upper() in article.title.upper():
                    result_list += [article]
            context_dict = {'result_list': result_list, 'query': query}
        if query == "":
            result_list = Article.objects.filter()
            context_dict = {'result_list': result_list, 'query': query}

    return render(request, 'lit/search.html', context_dict)


def show_article(request, article_name_slug):
    # Check if a logged in user is viewing this
    logged_in = False
    if request.user.is_authenticated():
        logged_in = True
    
    # Create a context dictionary in which we can pass
    # to the template rendering enginge.
    context_dict = {}

    # ARTICLE, COMMENTS, AND SNIPPETS DATA HANDLING
    try:
        # Can we find a article name slug with the given name?
        # If we can't, the .get() method rasises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises and exception.
        article = Article.objects.get(slug=article_name_slug)
        comments = Comment.objects.filter(article=article)
        snippets = Snippet.objects.filter(title=article)

        # We also add the article object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the article exists.
        context_dict['article'] = article
        context_dict['comments'] = comments
        context_dict['snippets'] = snippets
    except Article.DoesNotExist:
        # We get here if we didn't find the specified article.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['article'] = None
        context_dict['comments'] = None
        context_dict['snippets'] = None

    context_dict['favourited'] = False
    if logged_in == True:
        # FAVOURITE HANDLING
        # Test whether this user already has a Favourites object
        userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
        if Favourites.objects.filter(user=userprofile).exists():
            favouriteObject = Favourites.objects.get(user=userprofile)
            favourites = favouriteObject.fav_list.all()
            # Test whether this use has favourited this article
            if article in favourites:
                context_dict['favourited'] = True

        # COMMENT FORM HANDLING
        # If it's a HTTP POST, we're interested in processing form data.
        if request.method == 'POST':
            # Attempt to grab information from the raw form information.
            # Note that we make use of both ArticleForm.
            comment_form = CommentForm(data=request.POST)

            # If the form is valid...
            if comment_form.is_valid():
                # Since we need to set the img attribute ourselves,
                # we set commit=False. This delays saving the model
                # until we're read to avoid integrity problems.
                comment = comment_form.save(commit=False)
            
                # Set the comment's writer and article
                comment.user = userprofile
                comment.article = article

                # Now we save the Comment model instance.
                comment.save()
            else:
                # Invalid form - mistakes or something else?
                # Print problems to the terminal.
                print(comment_form.errors)

            comment_form = CommentForm()
        else:
            # Not a HTTP POST, so we render our form.
            # These forms will be blank, ready for user input.
            comment_form = CommentForm()
            
        context_dict['userprofile'] = userprofile
        context_dict['comment_form'] = comment_form
        
    return render(request, 'lit/article.html', context_dict)

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're read to avoid integrity problems.

            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'lit/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)
    
        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Literature Breakdown account is disabled.")
        else:
            user = User.objects.filter(username=username)
            if user:
                context_dict = {'error_message' : "Invalid password!"}
            else:
                context_dict = {'error_message' : "Invalid username!"}
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'lit/login.html', context_dict)
            #return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'lit/login.html', {})

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we an now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

def profile(request, username):
    context_dict = {}
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    articles = Article.objects.filter(author=userprofile)
    context_dict['userprofile'] = userprofile
    context_dict['articles'] = articles
    context_dict['numb_articles'] = len(articles)
    context_dict['selecteduser'] = user
    
    # If this user already has a favourites object then use it
    if Favourites.objects.filter(user=userprofile).exists():
        favourite = Favourites.objects.get(user=userprofile)
        favourites = favourite.fav_list.all()
        context_dict['favourites'] = favourites
        
    return render(request, 'lit/profile.html', context_dict)


def faq(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    return render(request, 'lit/faq.html', context_dict)


def new_articles(request):
    article_list_new = Article.objects.order_by('date_published')[:5]
    category_list = Category.objects.all()
    context_dict = {'articles_new': article_list_new,
                    'categories': category_list}
    return render(request, 'lit/new.html', context=context_dict)


def trending_articles(request):
    article_list_trending = Article.objects.order_by('-rating')[:5]
    category_list = Category.objects.all()
    context_dict = {'articles_trending' : article_list_trending,
                    'categories': category_list}
    return render(request, 'lit/trending.html', context=context_dict)

def show_category(request, category_name_slug):
    # Create a context dictionary in which we can pass
    # to the template rendering enginge.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method rasises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises and exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated pages.
        # Note that filter() will return a list of page objects or an empty list
        articles = Article.objects.filter(category=category)

        # Adds our results list to the template context under name pages.
        context_dict['articles'] = articles

        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify if we are looking at the same category
        context_dict['category'] = category

        # Pass the category list to display on the sidebar
        category_list = Category.objects.all()
        context_dict['categories'] = category_list
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['articles'] = None
        context_dict['category'] = None
        context_dict['categories'] = None
        
    return render(request, 'lit/category.html', context_dict)

@login_required
def add_article(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ArticleForm.
        article_form = ArticleForm(data=request.POST)

        # If the form is valid...
        if article_form.is_valid():
            # Since we need to set the img attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're read to avoid integrity problems.
            article = article_form.save(commit=False)

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'img' in request.FILES:
                article.img = request.FILES['img']

            # Set the article's writer
            userprofile = UserProfile.objects.get_or_create(user=user)[0]
            article.author = userprofile

            # Now we save the Article model instance.
            article.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
            
            return redirect('add_snippet', username=username, article_name_slug=article.slug)
        else:
            # Invalid form - mistakes or something else?
            # Print problems to the terminal.
            print(article_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        article_form = ArticleForm()

    # Render the template depending on the context.
    return render(request,
                   'lit/add_article.html',
                   {'article_form': article_form,
                   'registered': registered})

@login_required
def add_favourite(request, username, article_name_slug):
    # Check that user and article exist
    try:
        user = User.objects.get(username=username)
        article = Article.objects.get(slug=article_name_slug)
    except (User.DoesNotExist, Article.DoesNotExist) as error:
        print(error)
        return redirect('article')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    # If this user already has a favourites object then use it
    if Favourites.objects.filter(user=userprofile).exists():
        favourite = Favourites.objects.get(user=userprofile)
        favourites = favourite.fav_list.all()
        # If this artcile hasn't already been favourited then add it
        if article not in favourites:
            favourite.fav_list.add(article)
            favourite.save()
    # If this user doesn't have a favourites object then create it
    # and add the article
    else:
        favourite = Favourites.objects.create(user=userprofile)
        favourite.fav_list.add(article)
        favourite.save()   

    return redirect('show_article', article_name_slug=article_name_slug)

@login_required
def remove_favourite(request, username, article_name_slug):
    # Check that user and article exist
    try:
        user = User.objects.get(username=username)
        article = Article.objects.get(slug=article_name_slug)
    except (User.DoesNotExist, Article.DoesNotExist) as error:
        print(error)
        return redirect('article')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]

    # If this user already has a favourites object then use it
    if Favourites.objects.filter(user=userprofile).exists():
        favourite = Favourites.objects.get(user=userprofile)
        favourites = favourite.fav_list.all()
        # If this artcile has already been favourited then delete the instance
        if article in favourites:
            favourite.fav_list.remove(article)
            favourite.save()

    return redirect('show_article', article_name_slug=article_name_slug)

@login_required
def remove_comment(request, id, article_name_slug):
    # Check that user, article, and comment exist
    try:
        user = User.objects.get(username=request.user.username)
        article = Article.objects.get(slug=article_name_slug)
    except (User.DoesNotExist, Article.DoesNotExist) as error:
        print(error)
        return redirect('article')

    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]

    # If this user already has a comment object then delete it
    if Comment.objects.filter(user=userprofile).exists():
        Comment.objects.filter(id=id).delete()

    return redirect('show_article', article_name_slug=article_name_slug)

@login_required
def add_snippet(request, username, article_name_slug):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    # Create a context dictionary in which we can pass
    # to the template rendering enginge.
    context_dict = {}

    # ARTICLE, COMMENTS, AND SNIPPETS DATA HANDLING
    try:
        # Can we find a article name slug with the given name?
        # If we can't, the .get() method rasises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises and exception.
        article = Article.objects.get(slug=article_name_slug)
        snippets = Snippet.objects.filter(title=article)

        # We also add the article object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the article exists.
        context_dict['article'] = article
        context_dict['snippets'] = snippets
    except Article.DoesNotExist:
        # We get here if we didn't find the specified article.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['article'] = None
        context_dict['snippets'] = None
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both ArticleForm.
        snippet_form = SnippetForm(data=request.POST)

        # If the form is valid...
        if snippet_form.is_valid():
            # Get and save the Snippet
            snippet = snippet_form.save(commit=False)
            snippet.title = article
            snippet.save()

            # Reload the snippet form
            snippet_form = SnippetForm()
        else:
            # Invalid form - mistakes or something else?
            # Print problems to the terminal.
            print(snippet_form.errors)
    else:
        # Not a HTTP POST, so we render our form using the ModelForm instance.
        # These forms will be blank, ready for user input.
        snippet_form = SnippetForm()
        
    context_dict['snippet_form'] = snippet_form
    
    
        
    return render(request, 'lit/add_snippet.html', context_dict)

