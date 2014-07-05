from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from services import get_home_posts, get_post, get_user_posts
from forms import UserPostForm

def home(request):
    """
    Home page.
    """
    context = RequestContext(request)
    user = request.user
    context_dict = {}
    posts = get_home_posts()
    context_dict['posts'] = posts
    context_dict['user'] = user
    return render_to_response('posts/home.html', context_dict, context)
    
def each_post(request, post_id):
    """
    View for post page.
    """
    context = RequestContext(request)
    context_dict = {}
    post = get_post(post_id) # UserPosts.objects.get(id=post_id)
    if post is None:
        error = 'Page not found'
        return render_to_response('common/error.html', {'error':error}, context)
    context_dict['post'] = post
    return render_to_response('posts/post.html', context_dict, context)

@login_required
def add_post(request):
    """
    View that handles new posts that are posted.
    """
    context = RequestContext(request)
    current_user = request.user
    if request.method == 'POST':
        form = UserPostForm(request.POST)
        if form.is_valid():
            p1 = form.save(commit=False)
            p1.username_id = current_user.id
            p1.save()							
            return HttpResponseRedirect(reverse('home'))
        else:
            print form.errors
    else:
        form = UserPostForm()
        return render_to_response('posts/add_post.html', {'form':form}, context)

@login_required
def user_profile(request):
    """
    User profile page.
    """
    context = RequestContext(request)
    current_user = request.user
    context_dict = {}
    posts = get_user_posts(current_user.id)
    if posts:
        context_dict['posts'] = posts
        context_dict['user'] = current_user
        return render_to_response('posts/userprofile.html', context_dict, context)
    else:
        error = "No posts avaliable for the user "
        return render_to_response('common/error.html', {'error':error}, context)