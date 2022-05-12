import imp
import json

from bson.objectid import ObjectId

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from bitrix24 import bx24

from .forms import TemplateBoletoForm
from .models import TemplateBoleto, Boleto
from mongodb import querys
from rest_framework.authtoken.models import Token
from bitrix24.bitrix24 import update_robot
from pybitrix24 import Bitrix24
from btax.settings import CLIENT_ID, CLIENT_SECRET, DOMAIN
from functools import wraps
from btax.decorators import bitrix_auth


def consultar_boleto(request):
   pass


@login_required
def boletos_delete_all(request):
    querys.update_varios_objs(Boleto.COLLECTION_NAME, {'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO' }, { '$set':{ 'situacao': 'BAIXA'  }  }  )
    resp = HttpResponseRedirect(reverse('boletos:boletos-gerados'))
    return resp
@login_required
def boletos_gerados(request):
    print(str(request.user.profile.conta.cpf_cnpj))
    boletos = list(querys.filtra_objs(Boleto.COLLECTION_NAME, {'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO'}  ))
    
    #boletos_gerados = {}
    for result_object in boletos:
         print(result_object)
         #boletos_gerados[str(result_object.get('_id'))] = result_object
    resp =  render(request, 'boletos/templates/lista.html', 
        {
            'boletos_gerados': boletos
        }
    )
    # if 'delete_cookies' in request.GET: 
    #     ##resp.delete_cookie('token') 
    #     resp.delete_cookie('NOTIFICACAO_BITRIX')
    return resp




@login_required
#@bitrix_auth(bx24)
def templates_boletos(request):
    templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(request.user.profile.conta.id), 'deletado': False })
    resp =  render(request, 'boletos/templates/lista.html', 
        {
            'templates_boletos': templates_boletos
        }
    )
    return resp

@login_required
#@bitrix_auth(bx24)
def templates_boletos_novo(request):
    user_token = Token.objects.get(user=request.user).key
    bx24 = bx24.bitrixBtax(user_token)
    conta = request.user.profile.conta

    if request.method == 'POST':
        
        form = TemplateBoletoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            template = TemplateBoleto(conta_id=str(conta.id), **cleaned_data)
            querys.inserir_obj(TemplateBoleto.COLLECTION_NAME, template.dict_data())
            bx24.update_robot(token=user_token, account_id=conta.id, domain=request.META['HTTP_HOST'])
          
            return resp
        else:
            print('errors template form:', form.errors, flush=True)

    else:
        form = TemplateBoletoForm()

     
    resp = render(request, 'boletos/templates/cadastro.html',
        {
            'form': form,
        }
    )
    return resp

@login_required
#@bitrix_auth(bx24)
def templates_boletos_editar(request, template_boleto_id):
    conta = request.user.profile.conta
    user_token = Token.objects.get(user=request.user).key
    bx24 = bx24.bitrixBtax(user_token)
    template_boleto = querys.get_obj(TemplateBoleto.COLLECTION_NAME, {'_id': ObjectId(template_boleto_id), 'conta_id': str(conta.id)})
    if request.method == 'POST':
        form = TemplateBoletoForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            template = TemplateBoleto(_id=template_boleto['_id'], conta_id=str(conta.id), **cleaned_data)
            id_retorno = querys.update_obj(TemplateBoleto.COLLECTION_NAME, template._id, template.dict_data())
            
            bx24.update_robot(token=user_token, account_id=conta.id, domain=request.META['HTTP_HOST'])
           
            
        else:
            print('errors template form:', form.errors, flush=True)

    else:
        form = TemplateBoletoForm(initial=template_boleto)
    
    resp = render(request, 'boletos/templates/cadastro.html',
        {
            'form': form,
        }
    )
    # if 'delete_cookies' in request.GET:
    #     #resp.delete_cookie('token') 
    #     resp.delete_cookie('NOTIFICACAO_BITRIX')
    return resp

@login_required
#@bitrix_auth(bx24)
def templates_boletos_excluir(request, template_boleto_id):
    conta = request.user.profile.conta
    user_token = Token.objects.get(user=request.user).key
    bx24 = bx24.bitrixBtax(user_token)
    template_boleto = querys.get_obj(TemplateBoleto.COLLECTION_NAME, {'_id': ObjectId(template_boleto_id), 'conta_id': str(conta.id)})
    template_boleto['deletado'] = True
    querys.update_obj(TemplateBoleto.COLLECTION_NAME, template_boleto['_id'], template_boleto)
    bx24.update_robot(token=user_token, account_id=conta.id, domain=request.META['HTTP_HOST'])
    resp = redirect('boletos:boletos-gerados')
    return resp


@login_required
#@bitrix_auth(bx24)
def boletos_excluir(request, boleto_id):
    conta = request.user.profile.conta
    user_token = Token.objects.get(user=request.user).key
    bx24 = bx24.bitrixBtax(user_token)
    boleto = querys.get_obj(Boleto.COLLECTION_NAME, { 'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO' })
    boleto['situacao'] = 'FALHA'
    querys.update_obj(Boleto.COLLECTION_NAME, boleto['_id'], boleto)
    token = Token.objects.get(user=request.user)
    resp = redirect('boletos:boletos-gerados')
    
    
    return resp
