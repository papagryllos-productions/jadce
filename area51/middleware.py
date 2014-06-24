"""
Middleware classes.
We add an authentication class here, so we can auto-logout the deactivated users.
"""

from django.contrib.auth import logout

class StrictAuthentication:
    def process_view(self,request,view_func,view_args,view_kwargs):
        if request.user.is_authenticated() and not request.user.is_active:
            logout(request)
