# Import django modules
from django.urls import path

from . import views

app_name = 'autenticacao'

urlpatterns = [
	path('entrar/', views.entrar, name='entrar'),
    path('sair/', views.sair, name='sair'),
    path('criar-senha/<slug:user_id>/', views.criar_senha_primeiro_login, name='criar-senha'),
]