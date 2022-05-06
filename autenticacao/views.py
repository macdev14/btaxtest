# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import *
from .forms import *
from core.models import Profile

def entrar(request):
	next = request.GET.get('next', '/')
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return HttpResponseRedirect(next)
	else:
		form = LoginForm()
	return render(request, 'autenticacao/login.html', 
		{
			'form': form,
			'next': next
		}
	)

def sair(request):
	logout(request)
	return HttpResponseRedirect(reverse('autenticacao:entrar'))

def criar_senha_primeiro_login(request, user_id):
	usuario = get_object_or_404(User, id=user_id, is_first_login=True)
	if request.method == 'POST':
		form = UserFirstLoginForm(request.POST)
		if form.is_valid():
			cleaned_data = form.cleaned_data
			password = cleaned_data.get('password1')
			usuario.set_password(password)
			usuario.is_first_login = False
			usuario.save()

			messages.success(request, 'Senha criada com sucesso!')
			return HttpResponseRedirect(reverse('autenticacao:entrar'))
	else:
		form = UserFirstLoginForm()
	
	return render(request, 'autenticacao/criar-senha.html',
		{
			'form': form,
		}
	)