from django.conf.urls import patterns, url
from posts import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^post/(?P<post_title>\w+)$', views.each_post, name='post'),
)