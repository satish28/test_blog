from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import UserPosts

def home(request):
    context = RequestContext(request)
    user = request.user
    context_dict = {}
    posts = UserPosts.objects.all()
    context_dict['posts'] = posts
    context_dict['user'] = user
    return render_to_response('posts/home.html', context_dict, context)
    
def each_post(request, post_id):
    context = RequestContext(request)
    context_dict = {}
    post = UserPosts.objects.get(id=post_id)
    if post is None:
        error = 'Page not found'
        return render_to_response('common/error.html', error, context)
    context_dict['post'] = post
    return render_to_response('posts/post.html', context_dict, context)