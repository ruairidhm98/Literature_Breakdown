from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from lit.models import Member
from lit.models import Article
from lit.models import Comment
from lit.models import Snippet
from lit.models import Category
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

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, 'lit/search.html', {'result_list': result_list})


def show_article(request, article_name_slug):
    # Create a context dictionary in which we can pass
    # to the template rendering enginge.
    context_dict = {}

    try:
        # Can we find a article name slug with the given name?
        # If we can't, the .get() method rasises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises and exception.
        article = Article.objects.get(slug=article_name_slug)
        comments = Comment.objects.filter(article=article)
        snippets = Comment.objects.filter(title=article)

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
                  'rango/register.html',
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
                return HttpResponse("Your Rango account is disabled.")
        else:
            user = User.objects.filter(username=username)
            if user:
                context_dict = {'error_message' : "Invalid password!"}
            else:
                context_dict = {'error_message' : "Invalid username!"}
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return render(request, 'rango/login.html', context_dict)
            #return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we an now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))


def show_profile(request, user_name_slug):
    context_dict = {}

    try:
        # Can we find an username slug with the given name?
        # If we can't, the .get() method rasises a DoesNotExist exception.
        # So the .get() method returns one model instance or raises and exception.
        member = Member.objects.get(slug=user_name_slug)
        articles = Article.objects.filter(author=member)

        # We also add the article object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the article exists.
        context_dict['member'] = member
        context_dict['articles'] = articles
    except Member.DoesNotExist:
        # We get here if we didn't find the specified article.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['member'] = None
        context_dict['articles'] = None

    return render(request, 'lit/profile.html', context_dict)
