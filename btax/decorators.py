import imp
from django.shortcuts import render, reverse, get_object_or_404, redirect
from functools import wraps
import schedule

def bitrix_auth(bx24):
    def other_function(function):
        @wraps(function)
        def decorator(request, *args, **kwargs):
            try:
                bx24.obtain_token(request.COOKIES['bitrix_code'])['access_token']
                bx24.refresh_tokens()
                schedule.every(1).minutes.do(bx24.refresh_tokens)
            except:
                get_request = {}
                for k in request.GET.keys(): get_request[k]=request.GET[k]
                try:redirect(reverse(request.resolver_match.view_name, kwargs=get_request, args=[1]))
                except: redirect(reverse(request.resolver_match.view_name, kwargs=get_request))
                
              
            print(request)
            return function(request, *args, **kwargs)

        return decorator 
    return other_function