from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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
    pages = Paginator(posts_with_images,5)
    page = request.GET.get('page')
    try:
	    posts_pages = pages.page(page)
    except PageNotAnInteger:
	    posts_pages = pages.page(1)
    except EmptyPage:
	    posts_pages = pages.page(paginator.num_pages)
    context_dict['posts_images'] = posts_with_images
    context_dict['user'] = user
    context_dict['posts_pages'] = posts_pages
    return render_to_response('posts/home.html', context_dict, context)
    
def each_post(request, post_id):
    """
    View for post page.
    """
    context = RequestContext(request)
    user = request.user
    context_dict = {}
    post = get_post(post_id)
    if post is None:
        error = 'Page not found'
        return render_to_response('common/error.html', {'error':error}, context)
    increment_visit_count(post.id)
    context_dict['is_post_liked'] = is_post_liked(user, post)
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

def profiles(request,author):
    context = RequestContext(request)
    context_dict = {}
    current_user = request.user
    error = "No posts avaliable for the user "
    try:
	    user_id = User.objects.get(username=author)
    	posts = get_user_posts(user_id)
    except:
	    context_dict['error'] = error
	    return render_to_response('posts/profiles.html', context_dict, context)
    # Generating url for getting gravatar image.
    email = user_id.email
    image_size = 80
    gravatar_url = generate_gravatar_url(email, image_size)
    context_dict['gravatar_url'] = gravatar_url
    if posts:
	    context_dict['posts'] = posts
    else:
       	context_dict['error'] = error
    if str(current_user) == str(author):
	    context_dict['user'] = current_user
	    return render_to_response('posts/userprofile.html', context_dict, context)
    elif str(current_user) != str(author):
        context_dict['user_profile'] = author
        return render_to_response('posts/profiles.html', context_dict, context)        
    else:
        context_dict['error'] = error
        return render_to_response('posts/profiles.html', context_dict, context)
        
@login_required
def delete(request,post_id):
    delete_post(post_id)
    return HttpResponseRedirect(reverse('home'))

@login_required
def post_like(request):
    context = RequestContext(request)
    user = request.user
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']
        likes = update_likes(user, post_id)
    return HttpResponse(likes)
