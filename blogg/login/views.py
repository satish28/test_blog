from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from forms import UserRegisterForm
import logging

logger = logging.getLogger(__name__)


def user_login(request):
    context = RequestContext(request)
    error = ''
    if request.user.is_authenticated():
        user = request.user
        logger.debug('user [%s] authenticated' % (user.username))
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'POST':
        username = request.POST['username']    
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                logger.debug('user [%s] logged in' % (user.username))
                return HttpResponseRedirect(reverse('home'))
            else:
                logger.debug('user [%s] inactive' % (username))
                error = 'user inactive'
        else:
            logger.debug('user [%s] authentication failed' % (username))
            error = 'authentication failed'
    return render_to_response('login/login.html', {'error': error}, context)
    
def user_register(request):
    context = RequestContext(request)
    msg = ''
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            msg = "User created successfully"
            logger.debug('user [%s] created successfully' % (username))
        else:
            logger.debug('user [%s] creation failed' % (username))
            msg = form.errors
    else:
        form = UserRegisterForm()
    context_dict['form'] = form
    context_dict['msg'] = msg
    # Specify the url for register page
    return render_to_response('login/register.html', context_dict, context)
    
def user_logout(request):
    user = request.user
    logger.debug('user [%s] logging off...' % (user.username))
    return logout_then_login(request, reverse('home'))