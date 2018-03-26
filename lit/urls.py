from django.conf.urls import url
from lit import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'search/$', views.search, name='search'),
    url(r'^article/(?P<article_name_slug>[\w\-]+)/$', views.show_article, name='show_article'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name='show_category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^new/$', views.new_articles, name='new'),
    url(r'^trending/$', views.trending_articles, name='trending'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^add-article/(?P<username>[\w\-]+)/$', views.add_article, name='add_article'),
    url(r'^add-snippet/(?P<username>[\w-]+)/(?P<article_name_slug>[\w-]+)/$', views.add_snippet, name='add_snippet'),
    url(r'^add-favourite/(?P<username>[\w-]+)/(?P<article_name_slug>[\w-]+)/$', views.add_favourite, name='add_favourite'),
    url(r'^remove-favourite/(?P<username>[\w-]+)/(?P<article_name_slug>[\w-]+)/$', views.remove_favourite, name='remove_favourite'),
    url(r'^remove-comment/(?P<id>[\w-]+)/(?P<article_name_slug>[\w-]+)/$', views.remove_comment, name='remove_comment'),
    url(r'^edit-article/(?P<username>[\w-]+)/(?P<article_name_slug>[\w-]+)/$', views.edit_article, name='edit_article'),
    url(r'^remove_article/(?P<username>[\w-]+)/(?P<article_name_slug>[\w-]+)/$', views.remove_article, name='remove_article'),
    url(r'^edit-snippet/(?P<article_name_slug>[\w-]+)/(?P<snippet_id>[\w-]+)/$', views.edit_snippet, name='edit_snippet'),
    url(r'^remove-snippet/(?P<article_name_slug>[\w-]+)/(?P<snippet_id>[\w-]+)/$', views.remove_snippet, name='remove_snippet'),
    url(r'^edit-profile/$', views.edit_profile, name='edit_profile'),
    url(r'^remove-profile/$', views.remove_profile, name='remove_profile'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

