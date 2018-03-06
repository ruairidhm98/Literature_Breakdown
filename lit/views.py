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
from datetime import datetime

# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'lit/index.html', context=context_dict)

