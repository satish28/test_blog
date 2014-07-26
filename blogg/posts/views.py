from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from services import *
from forms import UserPostForm
import logging

logger = logging.getLogger(__name__)


def home(request):
    """
    Home page.
    """
    context = RequestContext(request)
    context_dict = {}
    posts = get_home_posts()
    posts_with_images = []
    image_size = 30
    for post in posts:
        post_with_image = PostWithImage(post, post.username.email, image_size)
        posts_with_images.append(post_with_image)
    pages = Paginator(posts_with_images, 5)
    page = request.GET.get('page')
    try:
	    posts_pages = pages.page(page)
    except PageNotAnInteger:
        logger.debug('page [%s] not an integer', page)
        posts_pages = pages.page(1)
    except EmptyPage:
        logger.debug('page [%s] empty', page)
        posts_pages = pages.page(Paginator.num_pages)
    context_dict['posts_images'] = posts_with_images
    context_dict['posts_pages'] = posts_pages
    # Getting popular authors
    popular_authors = get_popular_authors()
    logger.debug('popular authors count[%s]', len(popular_authors))
    context_dict['popular_authors'] = popular_authors
    # Getting popular posts
    popular_posts = get_popular_posts()
    logger.debug('popular posts count[%s]', len(popular_posts))
    context_dict['popular_posts'] = popular_posts
    return render_to_response('posts/home.html', context_dict, context)
    
def each_post(request, post_id):
    """
    View for post page.
    """
    context = RequestContext(request)
    current_user = request.user
    context_dict = {}
    post = get_post(post_id)
    if post is None:
        error = 'Page not found'
        logger.debug('Post [%s] not found', post_id)
        return render_to_response('common/error.html', {'error':error}, context)
    increment_visit_count(post.id)
    if str(current_user) == 'AnonymousUser':
        # Making is_post_liked true so that guest user cannot like a post. 
        # This is a simple hack.
        context_dict['is_post_liked'] = True
    else:
        context_dict['is_post_liked'] = is_post_liked(current_user, post)
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
            post_save = form.save(commit=False)
            post_save.username_id = current_user.id
            post_save.save()
            update_post_count(current_user)
            logger.debug('Post [%s] added by [%s]', post_save.id, current_user)							
            return HttpResponseRedirect(reverse('home'))
        else:
            logger.debug('Post cannot be added')
    else:
        form = UserPostForm()
        return render_to_response('posts/craft_post.html', {'form':form}, context)

def profile(request, author):
    context = RequestContext(request)
    context_dict = {}
    context_dict['name'] = author
    current_user = request.user
    error = "No posts avaliable for the user"
    try:
        user_id = User.objects.get(username=author)
        posts = get_user_posts(user_id)
        context_dict['posts'] = posts
    except Exception as e:
        logger.debug('No posts by this author [%s]', author)
        context_dict['error'] = error
        return render_to_response('posts/profile.html', context_dict, context)
    # Generating url for getting gravatar image.
    email = user_id.email
    image_size = 80
    gravatar_url = generate_gravatar_url(email, image_size)
    context_dict['gravatar_url'] = gravatar_url
    is_user_author = False
    if current_user.username == author:
        is_user_author = True
    context_dict['is_user_author'] = is_user_author
    return render_to_response('posts/profile.html', context_dict, context)
        
@login_required
def delete_post(request, post_id):
    current_user = request.user
    author = current_user.username
    hard_delete_post(post_id)
    logger.debug('Post [%s] by author [%s] deleted permanently', post_id, author)
    return HttpResponseRedirect(reverse('profile', kwargs={'author':author}))

@login_required
def edit_post(request, post_id):
    context = RequestContext(request)
    edit_form = UserPostForm(request.POST)
    edit_post = get_post(post_id)
    context_dict = {}
    context_dict['post'] = edit_post
    context_dict['form'] = edit_form
    if request.POST:
        edit_form=UserPostForm(request.POST, instance=edit_post)
        edit_form.save()	
        return HttpResponseRedirect(reverse('post', kwargs={'post_id':post_id}))
    else:
	    context_dict['form'] = UserPostForm(instance=edit_post)
    return render_to_response('posts/craft_post.html', context_dict, context)

@login_required
def post_like(request):
    context = RequestContext(request)
    current_user = request.user
    post_id = None
    if request.method == 'GET':
        post_id = request.GET['post_id']
        logger.info('post [%s] liked')
        likes = update_likes(current_user, post_id)
    return HttpResponse(likes)
