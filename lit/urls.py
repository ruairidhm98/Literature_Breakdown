from django.conf.urls import url
from lit import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'search/$', views.search, name='search'),
    url(r'^article/(?P<article_name_slug>[\w\-]+)/$',
        views.show_article, name='show_article'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',
        views.show_category, name='show_category'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^new/$', views.new_articles, name='new'),
    url(r'^trending/$', views.trending_articles, name='trending'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.profile, name='profile'),
    url(r'^add_article/$', views.add_article, name='add_article'),
    url(r'^add_article/(?P<username>[\w\-]+)/$', views.add_article, name='add_article'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

