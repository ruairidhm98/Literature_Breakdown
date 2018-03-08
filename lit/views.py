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
from lit.webhose_search import run_query


def index(request):
    article_list = Article.objects.order_by('-views')[:5]
    context_dict = {'articles': article_list}
    return render(request, 'lit/index.html', context=context_dict)


def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)

    return render(request, 'lit/search.html', {'result_list': result_list})
