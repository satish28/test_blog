from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import UserPosts
from forms import UserPostForm

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
        return render_to_response('common/error.html', {'error':error}, context)
    context_dict['post'] = post
    return render_to_response('posts/post.html', context_dict, context)

def add_post(request):
	if request.user.is_authenticated():
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
		return render_to_response('posts/add_post.html',{'form':form},context)
	else:
		return HttpResponse("User is not authenticated")

def user_profile(request):
	if request.user.is_authenticated():
		current_user = request.user
		context = RequestContext(request)
		context_dict = {}
		post = UserPosts.objects.filter(username_id=current_user.id)
		if post:
			context_dict['post'] = post
			context_dict['user'] = current_user
			return render_to_response('posts/userprofile.html', context_dict, context)
		else:
			error = "No posts avaliable for the user "
			return render_to_response('common/error.html', {'error':error}, context)
	else:
		context = RequestContext(request)
		error = "Please login"
		return render_to_response('common/error.html', {'error':error}, context)



