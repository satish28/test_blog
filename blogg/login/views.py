from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth import authenticate
from forms import UserRegisterForm
# Create your views here.

def user_login(request):
    context = RequestContext(request)
    error = ''
    if request.method == 'POST':
        username = request.POST['username']    
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print 'valid user'
                return HttpResponse('User authenticated successfully')
            else:
                print 'user is inactive'
                error = 'user inactive'
        else:
            print 'user authentication failed'
            error = 'authentication failed'
    return render_to_response('login/login.html', {'error':error}, context)
    
def user_register(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponse('User created successfully')
        else:
            print form.errors
    else:
        form = UserRegisterForm()
    return render_to_response('login/register.html', {'form': form}, context)
    
def user_logout(request):
    pass