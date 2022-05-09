from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    # ADMINISTRATIVO
   
    path('updateapp/', views.update_btax, name='update-btax'),
    path('installapp/', views.instalacao_btax, name='instalacao'),

    path('updateboleto/<uuid:id_negocio>', views.boleto_url_update, name='boleto-url-update'),
 
    path('contas/', views.contas, name='contas'),
    path('contas/novo/', views.contas_novo, name='contas-novo'),
    path('contas/editar/<uuid:conta_id>/', views.contas_editar, name='contas-editar'),
    path('contas/excluir/<uuid:conta_id>/', views.contas_excluir, name='contas-excluir'),
    path('contas/atualzar-token/<uuid:conta_id>/', views.contas_atualizar_token, name='contas-atualizar-token'),

    # CLIENTES
    path('empresas/', views.empresas, name='empresas'),
    path('empresas/novo/', views.empresas_novo, name='empresas-novo'),
    path('empresas/editar/<uuid:empresa_id>/', views.empresas_editar, name='empresas-editar'),
    path('empresas/excluir/<uuid:empresa_id>/', views.empresas_excluir, name='empresas-excluir'),

    path('servicos/', views.servicos, name='servicos'),
    path('servicos/novo/', views.servicos_novo, name='servicos-novo'),
    path('servicos/editar/<slug:servico_id>/', views.servicos_editar, name='servicos-editar'),
    path('servicos/excluir/<slug:servico_id>/', views.servicos_excluir, name='servicos-excluir'),

    path('', views.home, name='home'),
    #path('<str:url_name>', views.home, name='home-url'),
]
