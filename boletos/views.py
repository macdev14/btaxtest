import json

from bson.objectid import ObjectId

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .forms import TemplateBoletoForm
from .models import TemplateBoleto
from mongodb import querys
from rest_framework.authtoken.models import Token
from bitrix24.bitrix24 import update_robot
from pybitrix24 import Bitrix24
from btax.settings import CLIENT_SECRET_LOCAL, CLIENT_ID_LOCAL, CLIENT_ID, CLIENT_SECRET, DOMAIN
from functools import wraps
from btax.decorators import bitrix_auth

#remoto:
bx24 = Bitrix24(DOMAIN, CLIENT_ID, CLIENT_SECRET)
#local:
#bx24 = Bitrix24(DOMAIN, CLIENT_ID_LOCAL, CLIENT_SECRET_LOCAL)


@login_required
@bitrix_auth(bx24)
def templates_boletos(request):
    templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(request.user.profile.conta.id), 'deletado': False })
    return render(request, 'boletos/templates/lista.html', 
        {
            'templates_boletos': templates_boletos
        }
    )

@login_required
@bitrix_auth(bx24)
def templates_boletos_novo(request):
    global bx24
    conta = request.user.profile.conta

    if request.method == 'POST':
        
        form = TemplateBoletoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            template = TemplateBoleto(conta_id=str(conta.id), **cleaned_data)
            querys.inserir_obj(TemplateBoleto.COLLECTION_NAME, template.dict_data())
            token = Token.objects.get(user=request.user)
            update_robot(token, conta.id, bx24, request.META['HTTP_HOST'])
            return HttpResponseRedirect(reverse('boletos:templates'))
        else:
            print('errors template form:', form.errors, flush=True)

    else:
        form = TemplateBoletoForm()

    return render(request, 'boletos/templates/cadastro.html',
        {
            'form': form,
        }
    )

@login_required
@bitrix_auth(bx24)
def templates_boletos_editar(request, template_boleto_id):
    conta = request.user.profile.conta
    template_boleto = querys.get_obj(TemplateBoleto.COLLECTION_NAME, {'_id': ObjectId(template_boleto_id), 'conta_id': str(conta.id)})
    if request.method == 'POST':
        form = TemplateBoletoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            template = TemplateBoleto(_id=template_boleto['_id'], conta_id=str(conta.id), **cleaned_data)
            id_retorno = querys.update_obj(TemplateBoleto.COLLECTION_NAME, template._id, template.dict_data())
            token = Token.objects.get(user=request.user)
            update_robot(token, conta.id, bx24, request.META['HTTP_HOST'])
            return HttpResponseRedirect(reverse('boletos:templates'))
        else:
            print('errors template form:', form.errors, flush=True)

    else:
        form = TemplateBoletoForm(initial=template_boleto)

    return render(request, 'boletos/templates/cadastro.html',
        {
            'form': form,
        }
    )

@login_required
@bitrix_auth(bx24)
def templates_boletos_excluir(request, template_boleto_id):
    conta = request.user.profile.conta
    template_boleto = querys.get_obj(TemplateBoleto.COLLECTION_NAME, {'_id': ObjectId(template_boleto_id), 'conta_id': str(conta.id)})
    template_boleto['deletado'] = True
    querys.update_obj(TemplateBoleto.COLLECTION_NAME, template_boleto['_id'], template_boleto)
    token = Token.objects.get(user=request.user)
    update_robot(token, conta.id, bx24, request.META['HTTP_HOST'])
    return HttpResponseRedirect(reverse('boletos:templates'))