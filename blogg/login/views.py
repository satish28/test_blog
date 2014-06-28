from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from forms import UserRegisterForm


def user_login(request):
    context = RequestContext(request)
    error = ''
    if request.user.is_authenticated():
        # Specify the url for home page
        user = request.user
        return HttpResponse('Already logged in as %s <a href="logout">Logout</a>' % user.get_short_name())
    if request.method == 'POST':
        username = request.POST['username']    
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                print 'valid user'
                # Specify the url for home page
                return HttpResponse('User %s authenticated successfully <a href="logout">Logout</a>' % user.get_short_name())
            else:
                print 'user is inactive'
                error = 'user inactive'
        else:
            print 'user authentication failed'
            error = 'authentication failed'
    # Specify the url for login page
    return render_to_response('login/login.html', {'error': error}, context)
    
def user_register(request):
    context = RequestContext(request)
    msg = ''
    context_dict = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            msg = 'User created successfully'
        else:
            print form.errors
    else:
        form = UserRegisterForm()
    context_dict['form'] = form
    context_dict['msg'] = msg
    # Specify the url for register page
    return render_to_response('login/register.html', context_dict, context)
    
def user_logout(request):
    return logout_then_login(request, reverse('login'))