from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.core.exceptions import PermissionDenied

def only_administrators(function):
    def wrap(request, *args, **kwargs):
        user = request.user
        if user.is_superuser or user.is_staff:
            return function(request, *args, **kwargs)
        raise PermissionDenied
    return wrap