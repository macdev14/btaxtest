from django.urls import path

from . import views

app_name='boletos'

urlpatterns = [
    path('templates/', views.templates_boletos, name='templates'),
    path('templates/novo/', views.templates_boletos_novo, name='templates-novo'),
    path('templates/editar/<slug:template_boleto_id>/', views.templates_boletos_editar, name='templates-editar'),
    path('templates/excluir/<slug:template_boleto_id>/', views.templates_boletos_excluir, name='templates-excluir'),
]
