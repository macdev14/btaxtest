from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.http import HttpResponse
from . import views

app_name='api'

def testre(request):
    print(request.POST)
    print(request)
    print(request.json())
    print(request.POST.items())
    return HttpResponse(request.POST.items())



urlpatterns = [
    #path('cobrancas/emitir/', views.CobrancaEmitir.as_view(), name='cobrancas-emitir'),
    path('cobrancas/emitir/', testre, name='cobrancas-emitir'),
    path('cobrancas/consultar/', views.CobrancaConsulta.as_view(), name='cobrancas-consulta'),
    
    path('boletos/recebe-notificacao/', views.BoletoRecebeNotificacao.as_view(), name='boletos-recebe-notificacao'),

    path('teste/', views.TesteList.as_view(), name='teste'),
]

urlpatterns = format_suffix_patterns(urlpatterns)