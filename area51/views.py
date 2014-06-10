from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404
from django import forms
from geoposition.forms import GeopositionField

import area51.models as M

# The main page
def home(request):
    latest_events = M.Event.objects.all().order_by('-date_of_creation')[:20]
    context = {'latest_events': latest_events}
    return render(request, 'area51/index.html', context)

# user profile view
def user(request, username):
    us = get_object_or_404(M.User, username=username)
    return render(request, 'area51/user.html', {'us': us})

# single event page
def event(request, given_id):
    event = get_object_or_404(M.Event, pk=given_id)
    return render(request, 'area51/event.html', {'event': event})

# Create a new account page
def create_account(request):
    return render(request, 'area51/create_account.html')

# a form for the new-event page
class EventForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget = forms.Textarea, required=False)
    position = GeopositionField()
    category = forms.ChoiceField(choices=M.ALIENCATEGORIES)
    photo = forms.ImageField(required=False)

# New event page
def new(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            HttpResponseRedirect('/thanks/')
        else:
            raise Http404
    else:
        form = EventForm()
    return render(request, 'area51/new.html', {'form': form})

# Auxiliary view for AJAX requests
def data(request):
    all_events   = M.Event.objects.all()
    count_all    = len(all_events)
    dealt_events = len(M.Event.objects.filter(dealt=True))
    first        = all_events[0]
    response  = "<p><strong>Events so far:</strong> " + str(count_all) + "</p>"
    response += "<p><strong>Checked events:</strong> " + str(dealt_events) + "</p>"
    response += "<p><strong>Latest event:</strong> " + str(first) + "</p>"
    return HttpResponse(response)

# API list of events
def event_list(request):
    if request.method == "GET":
        json_serializer = serializers.get_serializer("json")()
        events = json_serializer.serialize(M.Event.objects.all(), ensure_ascii=False)
        return HttpResponse(events)
    else:
        return HttpResponse('This url is to be used for GET req ONLY!!!')

# API list of usernames
def user_list(request):
    if request.method == "GET":
        usernames = [o.username for o in M.User.objects.all()]
        return HttpResponse(",".join(usernames))
    else:
        return HttpResponse('This url is to be used for GET req ONLY!!!')

# POST view for creating a user
def adduser(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        # Let's check passwords first. This should probably happen in JS
        if request.POST['password1'] == request.POST['password2']:
            password = request.POST['password1']
        else:
            raise Http404

        # Phone is optional
        if not request.POST['phone']:
            phone = None
        else:
            phone = request.POST['phone']

        # Starting creation of user
        user = M.User.objects.create_user(first_name = request.POST['firstname'],
                                          last_name = request.POST['lastname'],
                                          email = request.POST['email'],
                                          telephone = phone,
                                          username = request.POST['username'],
                                          password = password)
        user.save()
        # Return the user to home page
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for editting a users profile
def edituser(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        # Finding the object in the DB
        us = M.User.objects.filter(username=request.user)
        if request.POST['firstname']:
            us.update(first_name=request.POST['firstname'])
        if request.POST['lastname']:
            us.update(last_name=request.POST['lastname'])
        if request.POST['email']:
            us.update(email=request.POST['email'])
        if request.POST['phone']:
            us.update(telephone=request.POST['phone'])

        # Return the user to his updated profile
        return HttpResponseRedirect('/u/' + str(request.user))
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for adding a new event
def addevent(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        if request.FILES:
            ph = request.FILES['photo']
        else:
            ph = None

        ev = M.Event.objects.create(title = request.POST['title'],
                                    creator = request.user,
                                    description = request.POST['description'],
                                    category = request.POST['category'],
                                    photo = ph)
        ev.position = request.POST['position_0'] + ',' + request.POST['position_1']
        ev.save()
        # Return the user to the home page
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
            return HttpResponseRedirect('/')
        else:
            raise Http404
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
