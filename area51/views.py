from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
import area51.models as M

# The main page
def home(request):
    latest_events = M.Event.objects.all().order_by('-date_of_creation')[:20]
    # these are the available variables inside the template:
    context = {'latest_events': latest_events}
    return render(request, 'area51/index.html', context)

# Create a new account page
def create_account(request):
    return render(request, 'area51/create.html')

# user profile view
def user(request, username):
    user = get_object_or_404(M.User, username=username)
    return render(request, 'area51/user.html', {'user': user})

# Auxiliary view for AJAX requests
def data(request):
    count = len(M.Event.objects.all())
    return HttpResponse(count)

# POST view for creating a user
def adduser(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        # Let's check passwords first. This should probably happen in JS
        if request.POST['password1'] == request.POST['password2']:
            password = request.POST['password1']
        else:
            return HttpResponse("Passwords don't match. TODO: better page.")
        # Starting creation of user
        user = M.User.objects.create_user(first_name = request.POST['firstname'],
                                          last_name = request.POST['lastname'],
                                          email = request.POST['email'],
                                          telephone = request.POST['phone'],
                                          username = request.POST['username'],
                                          password = password)
        user.save()
        # Return the user to home page
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for loging in
def homelogin(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        # return HttpResponse(request.POST['username'])
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # TODO: return to same page, but logged in
            return HttpResponseRedirect('/u/' + username)
        else:
            # TODO: return to no such account page
            return HttpResponse('Wrong username/password. TODO: better page')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for loging out
def homelogout(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')
