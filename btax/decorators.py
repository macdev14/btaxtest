from django.shortcuts import reverse, redirect
from functools import wraps
import schedule
from bitrix24.bitrix24 import *
from pybitrix24 import Bitrix24
from btax.settings import *
# def robot_schedule(request, bx24):
#     if request.COOKIES['token']: 
#         try: 
#             print("updating robot..")
#             update_robot(request.COOKIES['token'],request.user.profile.conta.id, bx24, request.META['HTTP_HOST'])
#             request.delete_cookie('token')
#         except: 
#             print('"Cookie robot update" exception')
#             raise Exception("Cookie robot update")
        
def notification_and_robot(request, bx24):
    
    if 'NOTIFICACAO_BITRIX' in request.COOKIES and request.COOKIES['NOTIFICACAO_BITRIX'] :
        bitrix24_user = bx24.call('user.current')['result']['ID']
        print(bx24.call('im.notify', {'to': int(bitrix24_user), 'message': str(request.COOKIES['NOTIFICACAO_BITRIX'])  }))
            
        

    if 'token' in request.COOKIES and request.COOKIES['token']: 
        print("updating robot..")
        print(update_robot(request.COOKIES['token'], request.user.profile.conta.id, bx24, request.META['HTTP_HOST']))
            
  
        
    

def bitrix_auth(bx24):
    def other_function(function):
        @wraps(function)
        def decorator(request, *args, **kwargs):
            try:
                # bx24 = Bitrix24(DOMAIN, CLIENT_ID, CLIENT_SECRET)

                # # #local:
                # if BITRIX_LOCAL:
                #      bx24 = Bitrix24(DOMAIN, CLIENT_ID_LOCAL, CLIENT_SECRET_LOCAL)
                # print("obtaining token: ")
                # print(bx24.obtain_tokens(request.COOKIES['bitrix_code'])['access_token'] )
                # bx24.refresh_tokens()
                print("tokens: ")
               
                if ('token' in request.COOKIES and request.COOKIES['token']) or ('NOTIFICACAO_BITRIX' in request.COOKIES and request.COOKIES['NOTIFICACAO_BITRIX']): 

                    notification_and_robot(request, bx24)
                    print('deleting cookies...')
                    request.GET._mutable = True
                    request.GET['delete_cookies'] = 'True'
                return request
                #schedule.every(1).minutes.do(bx24.refresh_tokens)
                #return data
                #schedule.every(5).minutes.do(robot_schedule(request, bx24))
                #schedule.every(30).seconds.do(notification(request, bx24))      
            except Exception as e:
                print(e)
                if not request.POST:
                    get_request = {}
                    for k in request.GET.keys(): get_request[k]=request.GET[k]
                    get_request['url_name'] = request.resolver_match.view_name
                    #print(get_request)
                    return redirect(reverse('core:home-url', kwargs=get_request))
                    #except: return redirect(reverse('core:home', kwargs=get_request))
                
              
            #print(request)
            return function(request, *args, **kwargs)

        return decorator 
    return other_function

    