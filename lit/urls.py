from django.conf.urls import url
from lit import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'search/$', views.search, name='search'),
    url(r'^article/(?P<article_name_slug>[\w\-]+)/$',
        views.show_article, name='show_article'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
