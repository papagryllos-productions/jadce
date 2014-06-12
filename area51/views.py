from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    contribution = get_object_or_404(M.Contribution, event_id=given_id)
    return render(request, 'area51/event.html', {'event': event, 'contribution': contribution})

# Create a new account page
def create_account(request):
    return render(request, 'area51/create_account.html')

# a form for the new-event page
class EventForm(forms.Form):
    title = forms.CharField(max_length=100, required=True)
    description = forms.CharField(widget = forms.Textarea, required=False)
    position = GeopositionField()
    category = forms.ChoiceField(choices=M.ALIENCATEGORIES)
    photo1 = forms.ImageField(required=False)
    photo2 = forms.ImageField(required=False)
    photo3 = forms.ImageField(required=False)
    photo4 = forms.ImageField(required=False)

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

# Event list view. Either displays user's events, or all o' them if he's a moderator
@login_required
def list_page(request):
    if request.user.is_superuser:
        opened = M.Event.objects.all().filter(dealt=False).order_by('-date_of_creation')
        # This is what we need to get all the info for the completed events:
        contributions = M.Contribution.objects.all()
        context = {"opened": opened, "contributions": contributions}
    else:
        user_latest = M.Event.objects.all().filter(creator=request.user).order_by('-date_of_creation')
        context = {"user_latest": user_latest}
    return render(request, 'area51/list.html', context)

# Auxiliary view for AJAX requests
def data(request):
    # Basic data
    all_events   = M.Event.objects.all()
    count_all    = len(all_events)
    dealt_events = len(M.Event.objects.filter(dealt=True))
    open_events  = count_all - dealt_events
    first        = all_events[0]

    # Time-average until completion/checking
    sumd = 0
    first_time = True
    all_contribs = M.Contribution.objects.all()
    for co in all_contribs:
        # substructing datetime objects yields a timedelta object
        td = co.date_of_contrib - co.event_id.date_of_creation
        if first_time:
            # The first time we just create the timedelta object
            sumd = td
            first_time = False
        else:
            # All the subsequent times we just adding. Timedeltas can be added.
            sumd += td
    # They can also be divided by integers, and be pretty printed with srt()
    average = sumd / dealt_events

    # We return them as html since they get printed immediately
    response  = "<ul>"
    response += "<li><strong>Events so far:</strong> " + str(count_all) + "</li>"
    response += "<li><strong>Checked events:</strong> " + str(dealt_events) + "</li>"
    response += "<li><strong>Open events:</strong> " + str(open_events) + "</li>"
    response += "<li><strong>Latest event:</strong> " + str(first) + "</li>"
    response += "<li><strong>Average completion time:</strong> " + str(average) + "</li>"
    response += "</ul>"
    return HttpResponse(response)

# API list of events
def event_list(request):
    if request.method == "GET":
        json_serializer = serializers.get_serializer("json")()
        events = json_serializer.serialize(M.Event.objects.all()[:20], ensure_ascii=False)
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

# POST view for editting a users profile
def edituser(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        # Finding the object in the DB. We get the user from the request for security reasons.
        # This way in case of malicious request the only edit could happen on the logged it user.
        us = M.User.objects.get(username=request.user)
        if request.POST['firstname']:
            us.first_name = request.POST['firstname']
        if request.POST['lastname']:
            us.last_name = request.POST['lastname']
        if request.POST['email']:
            us.email = request.POST['email']
        if request.POST['phone']:
            us.telephone = request.POST['phone']
        us.save()

        # Return the user to his updated profile
        return HttpResponseRedirect('/u/' + str(request.user))
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for adding a new event
def addevent(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        p1 = p2 = p3 = p4 = None
        if request.FILES:
            if 'photo1' in request.FILES:
                p1 = request.FILES['photo1']
            if 'photo2' in request.FILES:
                p2 = request.FILES['photo2']
            if 'photo3' in request.FILES:
                p3 = request.FILES['photo3']
            if 'photo4' in request.FILES:
                p4 = request.FILES['photo4']

        ev = M.Event.objects.create(title = request.POST['title'],
                                    creator = request.user,
                                    description = request.POST['description'],
                                    category = request.POST['category'],
                                    photo1 = p1,
                                    photo2 = p2,
                                    photo3 = p3,
                                    photo4 = p4)

        ev.position = request.POST['position_0'] + ',' + request.POST['position_1']
        ev.save()
        # Return the user to the home page
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for checking an event
def checkevent(request, given_id):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
        event = M.Event.objects.get(pk=given_id)
        if 'comment' in request.POST:
            com = request.POST['comment']
        else:
            com = ""
        # Create the contribution object
        contrib = M.Contribution.objects.create(admin_name = request.user,
                                                event_id   = event,
                                                comment    = com)
        # Marking it as checked/dealt
        event.dealt = True
        event.save()
        # Redirecting to the same page
        return HttpResponseRedirect('/list/')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for loging in
def homelogin(request):
    c = {}
    c.update(csrf(request))
    if request.method == "POST":
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
