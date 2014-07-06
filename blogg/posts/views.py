from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from services import *
from forms import UserPostForm

def home(request):
    """
    Home page.
    """
    context = RequestContext(request)
    user = request.user
    context_dict = {}
    posts = get_home_posts()
    posts_with_images = []
    image_size = 30
    for post in posts:
        post_with_image = PostWithImage(post, post.username.email, image_size)
        posts_with_images.append(post_with_image)
    context_dict['posts_images'] = posts_with_images
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
    increment_visit_count(post.id)
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
    # Generating url for getting gravatar image.
    email = current_user.email
    image_size = 80
    gravatar_url = generate_gravatar_url(email, image_size)
    context_dict['gravatar_url'] = gravatar_url
    context_dict['user'] = current_user
    if posts:
        context_dict['posts'] = posts
        return render_to_response('posts/userprofile.html', context_dict, context)
    else:
        error = "No posts avaliable for the user "
        context_dict['posts'] = posts
        context_dict['error'] = error
        return render_to_response('posts/userprofile.html', context_dict, context)

@login_required
def post_like(request):
    context = RequestContext(request)
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']
        likes = update_likes(post_id)
    return HttpResponse(likes)