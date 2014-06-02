from django.contrib import admin
from area51.models import User, Event, Contribution

admin.site.register(Event)
admin.site.register(User)
admin.site.register(Contribution)
