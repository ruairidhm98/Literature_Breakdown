from django.shortcuts import render
<<<<<<< HEAD
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from lit.models import Member
from lit.models import Article
from lit.models import Comment
from lit.models import Snippet
from datetime import datetime


#def user_login(request):
 #   if request.method == 'POST':
  #      username = request.POST.get('username')
   #     password = request.POST.get('password')

    #    user = authenticate(username=username, password=password)


def register(request):
    # Shows wether registration was successful
    registered = False

    # If it's HTTP POST, we want the info from the form
=======
from django.http import HttpResponse

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'lit/index.html', context=context_dict)
>>>>>>> 09c6b25422bf364cf76ed15d1354ab46ee846d5a
