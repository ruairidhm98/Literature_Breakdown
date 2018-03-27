from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from lit.models import *
from lit.forms import *
from datetime import datetime


###################### FRONTPAGE VIEWS ######################

def index(request):
    # Get 5 trending and new articles to display, as well as the categories
    article_list_trending = Article.objects.order_by('-rating')[:5]
    article_list_new = Article.objects.order_by('-date_published')[:5]
    category_list = Category.objects.all()

    # Fill the context dictionary and render the page
    context_dict = {'articles_new': article_list_new,
                    'articles_trending' : article_list_trending,
                    'categories': category_list}
    return render(request, 'lit/index.html', context=context_dict)


def search(request):
    result_list_articles = [] # List of articles found by search
    result_list_users = [] # List of users found by search

    # Process the search query
    if request.method == 'POST':
        query = request.POST['query'].strip()
        # If we have a valid query, get the articles and users that have a string in common
        # with the query to return
        if query:
            articles = Article.objects.filter()
            for article in articles:
                if query.upper() in article.title.upper():
                    result_list_articles += [article]
            users = UserProfile.objects.filter()
            for user in users:
                if query.upper() in user.name.upper() or query.upper() in user.user.username.upper():
                    result_list_users += [user]

        # If the query is an empty string return all the articles and users
        if query == "":
            result_list_articles = Article.objects.filter()
            result_list_users = UserProfile.objects.filter()
    
    # Sort the article and user list to display
    result_list_articles = sorted(result_list_articles,  key = lambda article: article.title.upper())
    result_list_users = sorted(result_list_users, key = lambda user: user.name.upper())

    # Fill the context dictionary and render the page
    context_dict = {'result_list_articles': result_list_articles,
                    'result_list_users': result_list_users,
                    'query': query}
    return render(request, 'lit/search.html', context_dict)

def faq(request):
    # Get the list of categories, fill the context dictionary and render the page
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    return render(request, 'lit/faq.html', context_dict)


def new_articles(request):
    # Get the list of new articles, categories, and the current date, then fill the context dictionary
    # and render the page
    article_list_new = Article.objects.order_by('-date_published')[:5]
    category_list = Category.objects.all()
    date_today = datetime.now().strftime("%d/%m/%Y")
    context_dict = {'articles_new': article_list_new,
                    'categories': category_list,
                    'date_today': date_today}
    return render(request, 'lit/new.html', context=context_dict)


def trending_articles(request):
    # Get the list of trending articles, categories, and the current date, then fill the context dictionary
    # and render the page
    article_list_trending = Article.objects.order_by('-rating')[:5]
    category_list = Category.objects.all()
    date_today = datetime.now().strftime("%d/%m/%Y")
    context_dict = {'articles_trending' : article_list_trending,
                    'categories': category_list,
                    'date_today': date_today}
    return render(request, 'lit/trending.html', context=context_dict)

def show_category(request, category_name_slug):
    # Create a context dictionary in which we can pass
    # to the template rendering enginge.
    context_dict = {}

    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises and exception.
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all of the associated articles.
        # Note that filter() will return a list of article objects or an empty list
        articles = Article.objects.filter(category=category)

        # Adds our results list to the template context under name articles.
        context_dict['articles'] = articles

        # We also add the category object from the database to the context dictionary.
        # We'll use this in the template to verify if we are looking at the same category
        context_dict['category'] = category

        # Pass the category list to display on the sidebar
        category_list = Category.objects.all()
        context_dict['categories'] = category_list
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything - the template will display the "no category" message for us.
        context_dict['articles'] = None
        context_dict['category'] = None
        context_dict['categories'] = None

    return render(request, 'lit/category.html', context_dict)




###################### USER AUTHENTICATION VIEWS ######################

def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. 
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

            login(request, user)
            return redirect('profile', username=user.username)
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
        # will raise a KeyError exception.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None, no user with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect('profile', username=user.username)
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
    else:
        # No context variables to pass to the template system
        return render(request, 'lit/login.html', {})

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we an now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))





###################### PROFILE VIEWS ######################

def profile(request, username):
    # Check if the user exists before rendering their profile
    try:
        user = User.objects.get(username=username)
    except (User.DoesNotExist) as error:
        print(error)
        return redirect('index')
    
    # Get all the relevant data on the user's profile to pass to the template
    context_dict = {}
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    articles = Article.objects.filter(author=userprofile)
    context_dict['userprofile'] = userprofile
    context_dict['articles'] = articles
    context_dict['numb_articles'] = len(articles)
    context_dict['selecteduser'] = user

    # If this user already has a favourites object then get it
    if Favourites.objects.filter(user=userprofile).exists():
        favourite = Favourites.objects.get(user=userprofile)
        favourites = favourite.fav_list.all()
        context_dict['favourites'] = favourites

    # Render the template depending on the context.
    return render(request, 'lit/profile.html', context_dict)

@login_required
def edit_profile(request):
    # Check if the user exists before edithing their profile
    try:
        user = User.objects.get(username=request.user.username)
    except (User.DoesNotExist) as error:
        print(error)
        return redirect('index')

    # Get all the relevant data on the user's profile as well as the needed forms
    # to pass to the template
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    user_form = UserForm(request.POST or None, instance=user)
    profile_form = UserProfileForm(request.POST or None, instance=userprofile)

    # If the two forms are valid...
    if user_form.is_valid() and profile_form.is_valid():
        # Save the user's form data to the database.
        user = user_form.save(commit=False)

        # Now we hash the password with the set_password method.
        # Once hashed, we can update the user object.
        user.set_password(user.password)
        user.save()

        # Now sort out the UserProfile instance.
        # Since we need to set the user attribute ourselves,
        # we set commit=False. This delays saving the model
        # until we're read to avoid integrity problems.
        userprofile = profile_form.save(commit=False)
        userprofile.user = user

        # Did the user provide a profile picture?
        # If so, we need to get it from the input form and
        # put it in the UserProfile model.
        if 'picture' in request.FILES:
            userprofile.picture = request.FILES['picture']

        # Now we save the UserProfile model instance.
        userprofile.save()

        # Log the user back in after having changed their data
        login(request, user)
            
        return redirect('profile', username=user.username)
    else:
        # Invalid form - mistakes or something else?
        # Print problems to the terminal.
        print(user_form.errors, profile_form.errors)
        

    # Render the template depending on the context.
    return render(request,
                  'lit/edit_profile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})

@login_required
def remove_profile(request):
    # Check if the user exists before deleting their profile
    try:
        user = User.objects.get(username=request.user.username)
    except (User.DoesNotExist) as error:
        print(error)
        return redirect('index')

    # Delete the user's UserProfile as well as their User object
    if UserProfile.objects.filter(user=user).exists():
        User.objects.filter(username=user.username).delete()
        UserProfile.objects.filter(user=user).delete()

    return redirect('profile', username=user.username)





###################### ARTICLE VIEWS ######################

def show_article(request, article_name_slug):
    # Check if a logged in user is viewing this
    logged_in = False
    if request.user.is_authenticated():
        logged_in = True
    
    # Create a context dictionary in which we can pass
    # to the template rendering enginge.
    context_dict = {}

    # ARTICLE, COMMENTS, AND SNIPPETS DATA HANDLING #
    try:
        # Get all the relevant data on the article to pass to the template
        article = Article.objects.get(slug=article_name_slug)
        comments = Comment.objects.filter(article=article)
        snippets = Snippet.objects.filter(title=article)
        context_dict['article'] = article
        context_dict['comments'] = comments
        context_dict['snippets'] = snippets
    except Article.DoesNotExist:
        # If we can't find the specified article then return nothing
        context_dict['article'] = None
        context_dict['comments'] = None
        context_dict['snippets'] = None

    context_dict['favourited'] = False
    if logged_in == True:
        # FAVOURITE HANDLING #
        # Test whether this user already has a Favourites object
        userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
        if Favourites.objects.filter(user=userprofile).exists():
            # If so then test whether this user has favourited the article
            favouriteObject = Favourites.objects.get(user=userprofile)
            favourites = favouriteObject.fav_list.all()
            if article in favourites:
                context_dict['favourited'] = True

        # COMMENT FORM HANDLING #
        # Check if the user has already commented on this article
        can_comment = True
        if (Comment.objects.filter(article=article, user=userprofile).exists()) or (article.author==userprofile):
            # If so then set can_comment to False so they can't comment a second time
            can_comment = False
        context_dict['can_comment'] = can_comment
        
        # If it's a HTTP POST, we're interested in processing form data.
        if request.method == 'POST':
            # Get the comment data from the comment form
            comment_form = CommentForm(data=request.POST)

            # If the form is valid...
            if comment_form.is_valid():
                # Since we need to set the user and article attributes
                # ourselves, we set commit=False.
                comment = comment_form.save(commit=False)
            
                # Set the comment's writer and article and save it
                comment.user = userprofile
                comment.article = article
                comment.save()

                # Update the article's average rating
                comments = Comment.objects.filter(article=article)
                rating_count = 0
                rating = 0
                for comment in comments:
                    rating += comment.rating
                    rating_count += 1
                rating = rating/rating_count
                rating = round(rating,1)
                article.rating = rating
                article.save()
            else:
                # If the form is invalid, print the error to the terminal
                print(comment_form.errors)
        else:
            # Not a HTTP POST, so we render our form.
            # These forms will be blank, ready for user input.
            comment_form = CommentForm()
            
        context_dict['userprofile'] = userprofile
        context_dict['comment_form'] = comment_form

    # Render the template depending on the context.
    return render(request, 'lit/article.html', context_dict)

@login_required
def add_article(request, username):
    # Check if the user exists before adding an article
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    
    # A boolean value for telling the template
    # whether the registration was successful.
    registered = False
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Get the article data from the article form
        article_form = ArticleForm(data=request.POST)

        # If the form is valid...
        if article_form.is_valid():
            # Since we need to set the img attribute ourselves,
            # we set commit=False
            article = article_form.save(commit=False)

            # Did the user provide a profile picture?
            # If so, put it in the article model.
            if 'img' in request.FILES:
                article.img = request.FILES['img']

            # Set the article's writer, author, and date published, then save it
            userprofile = UserProfile.objects.get_or_create(user=user)[0]
            article.author = userprofile
            article.date_published = datetime.now().strftime("%d/%m/%y")
            article.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True

            # Proceed to the add snippet page
            return redirect('add_snippet', username=username, article_name_slug=article.slug)
        else:
            # If the form is invalid, print the error to the terminal
            print(article_form.errors)
    else:
        # Not a HTTP POST, so we render the empty article form
        article_form = ArticleForm()

    # Render the template depending on the context.
    return render(request,
                   'lit/add_article.html',
                   {'article_form': article_form,
                   'registered': registered})

@login_required
def edit_article(request, username, article_name_slug):
    # Check that user and article exist before editing
    try:
        user = User.objects.get(username=request.user.username)
        article = Article.objects.get(slug=article_name_slug)
    except (User.DoesNotExist, Article.DoesNotExist) as error:
        print(error)
        return redirect('index')

    # Create the article form and fill it with preexisting article data
    article = get_object_or_404(Article, slug=article_name_slug)
    article_form = ArticleForm(request.POST or None, instance=article)

    # If the user put something in the form
    if article_form.is_valid():
        # Since we need to set the img attribute ourselves,
        # we set commit=False.
        article = article_form.save(commit=False)

        # Did the user provide a profile picture?
        # If so, put it in the article model.
        if 'img' in request.FILES:
                article.img = request.FILES['img']

        # Set the article's writer and save it
        userprofile = UserProfile.objects.get_or_create(user=user)[0]
        article.author = userprofile
        article.save()
        
        # Update our variable to indicate that the template
        # registration was successful.
        registered = True

        # Proceed to the add snippet page
        return redirect('add_snippet', username=username, article_name_slug=article.slug)
    else:
        # If the form is invalid, print the error to the terminal
        print(article_form.errors)

    # Render the template depending on the context.
    return render(request,
                   'lit/edit_article.html',
                   {'article_form': article_form,
                    'article': article})
                
@login_required
def remove_article(request, username, article_name_slug):
    # Check that user and article exist before removing the article
    try:
        user = User.objects.get(username=request.user.username)
        article = Article.objects.get(slug=article_name_slug)
    except (User.DoesNotExist, Article.DoesNotExist) as error:
        print(error)
        return redirect('index')

    # Find the article in the DB and delete it
    userprofile = UserProfile.objects.get_or_create(user=request.user)[0]
    if Article.objects.filter(author=userprofile).exists():
        Article.objects.filter(title=article.title).delete()

    # Return to the user's profile
    return redirect('profile', username=username)




###################### FAVOURITE VIEWS ######################

@login_required
def add_favourite(request, username, article_name_slug):
    # Check that user and article exist before adding a favourite
    try:
        user = User.objects.get(username=username)
        article = Article.objects.get(slug=article_name_slug)
    except (User.DoesNotExist, Article.DoesNotExist) as error:
        print(error)
        return redirect('index')

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

    # Return to the article page
    return redirect('show_article', article_name_slug=article_name_slug)

@login_required
def remove_favourite(request, username, article_name_slug):
    # Check that user and article exist before removing the favourite
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

    # Return to the article page
    return redirect('show_article', article_name_slug=article_name_slug)




###################### COMMENT VIEWS ###################### (Comment adding handled in show_article) 

@login_required
def remove_comment(request, id, article_name_slug):
    # Check that user, article, and comment exist before removing the comment
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

        # Update article average rating
        if Comment.objects.filter(article=article).exists():
            comments = Comment.objects.filter(article=article)
            rating_count = 0
            rating = 0
            for comment in comments:
                rating += comment.rating
                rating_count += 1
            rating = rating/rating_count
            rating = round(rating,1)
            article.rating = rating
            article.save()

    # Go back to the article page
    return redirect('show_article', article_name_slug=article_name_slug)





###################### SNIPPET VIEWS ######################

@login_required
def add_snippet(request, username, article_name_slug):
    # Check that user exists before adding a snippet
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')

    context_dict = {}

    try:
        # Check that the article exists and get it along with preexisting snippets
        article = Article.objects.get(slug=article_name_slug)
        snippets = Snippet.objects.filter(title=article)

        # Get all the relevant data on the article and snippets to pass to the template
        context_dict['article'] = article
        context_dict['snippets'] = snippets
    except Article.DoesNotExist:
        # If the article doesn't exist the return nothing
        context_dict['article'] = None
        context_dict['snippets'] = None
    
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
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
            # If the form is invalid, print the error to the terminal
            print(snippet_form.errors)
    else:
        # Not a HTTP POST, so we render our form
        snippet_form = SnippetForm()
        
    context_dict['snippet_form'] = snippet_form

    # Render the template depending on the context.
    return render(request, 'lit/add_snippet.html', context_dict)

@login_required
def edit_snippet(request, article_name_slug, snippet_id):
    # Check that article and snippet exist before editing it
    try:
        article = Article.objects.get(slug=article_name_slug)
        snippet = Snippet.objects.get(id=snippet_id)
    except (Article.DoesNotExist, Snippet.DoesNotExist) as error:
        print(error)
        return redirect('index')

    # Create the snippet form and fill it with preexisting snippet data
    context_dict = {}
    snippet = get_object_or_404(Snippet, id=snippet_id)
    snippet_form = SnippetForm(request.POST or None, instance=snippet)

    # If what the user inserted in the form is correct
    if snippet_form.is_valid():
        # Delete the pre-existing snippet
        Snippet.objects.filter(id=snippet_id).delete()
        
        # Get and save the new Snippet
        snippet = snippet_form.save(commit=False)
        snippet.title = article
        snippet.save()

        # Return to the article page
        return redirect('show_article', article_name_slug=article.slug)
    else:
        # If the form is invalid print its errors to the terminal
        print(snippet_form.errors)

    # Pass the article and snippet data, and the form to the context_dictionary
    context_dict['article'] = article
    context_dict['snippet'] = snippet
    context_dict['snippet_form'] = snippet_form

    # Render the template depending on the context.
    return render(request, 'lit/edit_snippet.html', context_dict)

@login_required
def remove_snippet(request, article_name_slug, snippet_id):
    # Check that article and snippet exist before deleting it
    try:
        article = Article.objects.get(slug=article_name_slug)
        snippet = Snippet.objects.get(id=snippet_id)
    except (Article.DoesNotExist, Snippet.DoesNotExist) as error:
        print(error)
        return redirect('index')

    # If the snippet exists then delete it
    if Snippet.objects.filter(id=snippet_id).exists():
        Snippet.objects.filter(id=snippet_id).delete()

    # Return to the article page
    return redirect('show_article', article_name_slug=article_name_slug)

