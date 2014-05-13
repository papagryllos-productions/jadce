from django.shortcuts import render, get_object_or_404
# the one above includes:
# from django.template import RequestContext, loader
# from django.http import HttpResponse

from area51.models import User

def home(request):
    # using django db api
    latest_users = User.objects.all().order_by('-phone')[:5]
    context = {'latest_users': latest_users}
    return render(request, 'area51/index.html', context)

def details(request, username):
    user = get_object_or_404(User, pk=username)
    return render(request, 'area51/details.html', {'user': user})
