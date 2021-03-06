"""
Connection interface between models (DB - backend) and templates (frontend)
"""

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

import area51.models as M
from area51.forms import EventForm

# The main page
def home(request):
    latest_events = M.Event.objects.all().order_by('date_of_creation').reverse()[:20]
    context = {'latest_events': latest_events}
    return render(request, 'area51/index.html', context)

# user profile view
def user(request, username):
    us = get_object_or_404(M.User, username=username)
    return render(request, 'area51/user.html', {'us': us})

# single event page
def event(request, given_id):
    event = get_object_or_404(M.Event, pk=given_id)
    if event.dealt:
        contribution = get_object_or_404(M.Contribution, event_id=given_id)
        return render(request, 'area51/event.html', {'event': event, 'contribution': contribution})
    else:
        return render(request, 'area51/event.html', {'event': event})

# Create a new account page
def create_account(request):
    return render(request, 'area51/create_account.html')

# New event page
@login_required
def new(request):
    form = EventForm()
    # Need to pull the categories from the DB to get them available
    objs = M.Aliencategories.objects.all()
    available_choices = [obj.name for obj in objs]
    return render(request, 'area51/new.html', {'form': form, 'categories': available_choices})

# Event list view. Either displays user's events, or all o' them if he's a moderator
@login_required
def list_page(request):
    if request.user.is_superuser:
        open_events = M.Event.objects.all().filter(dealt=False).order_by('-date_of_creation')

        # Paginating with 20 elements per page.
        paginator = Paginator(open_events, 20)
        page = request.GET.get('page')    # Getting and processing the requested page number.
        try:
            paginated_open = paginator.page(page)
        except PageNotAnInteger:
            paginated_open = paginator.page(1)
        except EmptyPage:
            paginated_open = paginator.page(paginator.num_pages)

        # We need to deliver the categories as well
        categories = [event.category for event in paginated_open]
        categories = list(set(categories))    # keeping unique items

        # This is what we need to get all the info for the completed events:
        contributions = M.Contribution.objects.all()

        context = {"open_events": paginated_open, "categories": categories, "contributions": contributions}
    else:
        user_latest = M.Event.objects.all().filter(creator=request.user).order_by('-date_of_creation')
        context = {"user_latest": user_latest}
    return render(request, 'area51/list.html', context)

###############################################################################
##########################         API calls         ##########################
###############################################################################

# Auxiliary view for AJAX requests
def data(request):
    # Basic data
    all_events   = M.Event.objects.all()
    number_all   = len(all_events)
    number_dealt = len(M.Event.objects.filter(dealt=True))
    number_open  = number_all - number_dealt
    if number_all:
        # Finding time-average from event creation until completion/checking
        if number_dealt:
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
            # They can also be divided by integers, and be pretty-printed with srt()
            average = sumd / number_dealt
            # Prettifying
            list_average = str(average).split(":")
            list_average = list(map(float, list_average))
            pretty_average = ""
            if list_average[0] != 0:
                if list_average[0] == 1:
                    pretty_average += "%d hour," % list_average[0]
                else:
                    pretty_average += "%d hours," % list_average[0]
            if list_average[1] != 0:
                if list_average[1] == 1:
                    pretty_average += " %d minute" % list_average[1]
                else:
                    pretty_average += " %d minutes" % list_average[1]
        else:
            pretty_average = "No dealt events yet"

        # We return them as html since they get printed immediately
        response  = "<ul>"
        response += "<li><strong>Events so far:</strong> " + str(number_all) + "</li>"
        response += "<li><strong>Checked events:</strong> " + str(number_dealt) + "</li>"
        response += "<li><strong>Open events:</strong> " + str(number_open) + "</li>"
        response += "<li><strong>Average completion time:</strong> " + pretty_average + "</li>"
        response += "</ul>"
    else:
        response  = "<p>No events yet</p>"
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
        # Let's check passwords first. This should probably happen in JS too.
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
        # Log user in to his account
        logged_in = authenticate(username=request.POST['username'], password=password)
        login(request, logged_in)
        return HttpResponseRedirect('/')
    else:
        return HttpResponse('This url is to be used for POST req ONLY!!!')

# POST view for editting a users profile
@login_required
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
@login_required
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
@login_required
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
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse("User is deactivated. Please contact the administrator.")
        else:
            return HttpResponse("Wrong username/password")
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

###############################################################################
##########################           Admin           ##########################
###############################################################################

# moderator view
@login_required
def mod(request):
    # Only moderators allowed
    if not request.user.is_superuser:
        return HttpResponseRedirect('/')

    all_events = M.Event.objects.all()
    users = M.User.objects.all()
    count_all = len(all_events)
    dealt_events = len(M.Event.objects.filter(dealt=True))
    open_events  = count_all - dealt_events
    categories =  M.Aliencategories.objects.all()
    data = { 'dealt_events': dealt_events, 'open_events': open_events, 'all_events': all_events, 'users': users, 'categories': categories}
    return render(request, 'area51/moderator.html', data)

# POST view for moderator panel
@csrf_exempt
@login_required
def panel(request):
    # Only moderators allowed
    if not request.user.is_superuser:
        return HttpResponse('505 Forbidden. User is not a moderator.')

    if request.method == "POST":
        if 'pk' in request.POST:
            user = M.User.objects.get(pk=request.POST['pk'])
            if 'name' in request.POST:
                if request.POST['name'] == 'first_name':
                    user.first_name = request.POST['value']
                elif request.POST['name'] == 'last_name':
                    user.last_name = request.POST['value']
                elif request.POST['name'] == 'telephone':
                    user.telephone = request.POST['value']
                user.save()
                return HttpResponseRedirect('/moderator/')
            else:
                return HttpResponse('Wrong my friend')
        else:
            return HttpResponse('No user given')
    else:
        # Hack around get requests, so we wouldn't need an extra view
        user = M.User.objects.get(pk=request.GET['pk'])
        if 'name' in request.GET:
            if request.GET['name'] == 'is_active':
                if not user.is_superuser or request.user == user:
                    # Superusers can do everything on regular users
                    # and deactivate only themselves (not other superusers)
                    user.is_active = not user.is_active
            if request.GET['name'] == 'is_superuser':
                # We only can promote from here
                if not user.is_superuser:
                    user.is_superuser = True
            user.save()
            return HttpResponseRedirect('/moderator/')
        else:
            return HttpResponse('Wrong my friend')

# POST view for editting categories
@csrf_exempt
@login_required
def cat_panel(request):
    # Only moderators allowed
    if not request.user.is_superuser:
        return HttpResponse('505 Forbidden. User is not a moderator.')

    if request.method == "POST":
        if 'pk' in request.POST:
            cat_obj = M.Aliencategories.objects.get(pk=request.POST['pk'])
            if 'name' in request.POST:
                cat_obj.name = request.POST['value']
                cat_obj.save()
                return HttpResponseRedirect('/moderator/')
        elif 'cat_name' in request.POST:
            category = M.Aliencategories(name=request.POST['cat_name'])
            category.save()
            return HttpResponseRedirect('/moderator/')
    else:
        if 'pk' in request.GET:
            cat_obj = M.Aliencategories.objects.get(pk=request.GET['pk'])
        if 'name' in request.GET:
            if request.GET['name'] == 'delete':
                cat_obj.delete()
                return HttpResponseRedirect('/moderator/')
        return HttpResponse('No no')
