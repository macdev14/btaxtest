from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name='api'

urlpatterns = [
    path('cobrancas/emitir/', views.CobrancaEmitir.as_view(), name='cobrancas-emitir'),
    path('cobrancas/consultar/', views.CobrancaConsulta.as_view(), name='cobrancas-consulta'),
    
    path('boletos/recebe-notificacao/', views.BoletoRecebeNotificacao.as_view(), name='boletos-recebe-notificacao'),

    path('teste/', views.TesteList.as_view(), name='teste'),
]

urlpatterns = format_suffix_patterns(urlpatterns)