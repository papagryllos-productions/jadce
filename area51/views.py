from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render, get_object_or_404

import area51.models as M

# The main page
def home(request):
    # using django db api
    latest_users = M.User.objects.all().order_by('-phone')[:5]
    context = {'latest_users': latest_users}
    return render(request, 'area51/index.html', context)

# User profile page
def user(request, username):
    user = get_object_or_404(M.User, pk=username)
    return render(request, 'area51/user.html', {'user': user})

# Create a new account page
def create_account(request):
    return render(request, 'area51/create.html')

# Auxiliary view for AJAX requests
def data(request):
    count = len(M.Event.objects.all())
    return HttpResponse(count)
