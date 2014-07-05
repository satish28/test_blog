from django.conf.urls import patterns, url
from posts import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^post/(?P<post_id>\d+)$', views.each_post, name='post'),
    url(r'^add_post/$',views.add_post,name='add_post'),
    url(r'^userprofile/$',views.user_profile,name='user_profile'),
    url(r'^userprofile/post/(?P<post_id>\d+)$', views.each_post, name='post'),
)
