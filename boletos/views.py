import imp
import json

from bson.objectid import ObjectId

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

from .forms import TemplateBoletoForm
from .models import TemplateBoleto, Boleto
from mongodb import querys
from rest_framework.authtoken.models import Token
from bitrix24.bitrix24 import update_robot
from pybitrix24 import Bitrix24
from btax.settings import CLIENT_ID, CLIENT_SECRET, DOMAIN
from functools import wraps
from btax.decorators import bitrix_auth
from btax.config import bx24
#remoto:
#bx24 = Bitrix24(DOMAIN, CLIENT_ID, CLIENT_SECRET)
#local:
#bx24 = Bitrix24(DOMAIN, CLIENT_ID_LOCAL, CLIENT_SECRET_LOCAL)

# with bitrix_auth(bx24) as response:
#     response.delete_cookie('token')
#     response.delete_cookie('NOTIFICACAO_BITRIX')

def consultar_boleto(request):
   pass


# def url_boleto(request):
#     resp = HttpResponseRedirect(reverse('core:update-btax'))
#     #resp.set_cookie('token', token)
#     resp.set_cookie('VIEW_REDIRECT', 'core:url-boleto-btax')
@login_required
def boletos_delete_all(request):
<<<<<<< HEAD
    p = querys.update_varios_objs(Boleto.COLLECTION_NAME, {'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO' }, { '$set': {'situacao' : 'BAIXA' } }  )
=======
    querys.update_varios_objs(Boleto.COLLECTION_NAME, {'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO' }, { '$set':{ 'deletado': True  }  }  )
>>>>>>> debef6e (ls)
    resp = HttpResponseRedirect(reverse('boletos:boletos-gerados'))
    return resp
@login_required
def boletos_gerados(request):
    print(str(request.user.profile.conta.cpf_cnpj))
<<<<<<< HEAD
    boletos = list(querys.filtra_objs(Boleto.COLLECTION_NAME, {'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO'}  ))
=======
    boletos = list(querys.filtra_objs(Boleto.COLLECTION_NAME, {'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO', 'deletado': False }  ))
>>>>>>> debef6e (ls)
    
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
    # if 'delete_cookies' in request.GET: 
    #     ##resp.delete_cookie('token') 
    #     resp.delete_cookie('NOTIFICACAO_BITRIX')
    return resp

@login_required
#@bitrix_auth(bx24)
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
            #update_robot(token, conta.id, bx24, request.META['HTTP_HOST'])
            resp = HttpResponseRedirect(reverse('core:update-btax'))
            resp.set_cookie('token', token)
            resp.set_cookie('VIEW_REDIRECT', 'core:update-btax')
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
    # if 'delete_cookies' in request.GET: 
    #     #resp.delete_cookie('token') 
    #     resp.delete_cookie('NOTIFICACAO_BITRIX')
    return resp

@login_required
#@bitrix_auth(bx24)
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
            #update_robot(token, conta.id, bx24, request.META['HTTP_HOST'])
            resp = HttpResponseRedirect(reverse('core:update-btax'))
            resp.set_cookie('token', token)
            resp.set_cookie('VIEW_REDIRECT', 'core:update-btax')
            return resp
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
    template_boleto = querys.get_obj(TemplateBoleto.COLLECTION_NAME, {'_id': ObjectId(template_boleto_id), 'conta_id': str(conta.id)})
    template_boleto['deletado'] = True
    querys.update_obj(TemplateBoleto.COLLECTION_NAME, template_boleto['_id'], template_boleto)
    token = Token.objects.get(user=request.user)
    resp = HttpResponseRedirect(reverse('core:update-btax'))
    resp.set_cookie('VIEW_REDIRECT', 'core:update-btax')
    # if 'delete_cookies' in request.GET: 
    #     #resp.delete_cookie('token') 
    #     resp.delete_cookie('NOTIFICACAO_BITRIX')
    resp.set_cookie('token', token)
    
    return resp


@login_required
#@bitrix_auth(bx24)
def boletos_excluir(request, boleto_id):
    conta = request.user.profile.conta
    boleto = querys.get_obj(Boleto.COLLECTION_NAME, { 'cedente_cpf_cnpj': str(request.user.profile.conta.cpf_cnpj), 'situacao' : 'SALVO' })
<<<<<<< HEAD
    boleto['situacao'] = 'BAIXA'
=======
    boleto['situacao'] = 'FALHA'
>>>>>>> debef6e (ls)
    querys.update_obj(Boleto.COLLECTION_NAME, boleto['_id'], boleto)
    token = Token.objects.get(user=request.user)
    resp = HttpResponseRedirect(reverse('boletos:boletos-gerados'))
    resp.set_cookie('VIEW_REDIRECT', 'boletos:boletos-gerados')
    # if 'delete_cookies' in request.GET: 
    #     #resp.delete_cookie('token') 
    #     resp.delete_cookie('NOTIFICACAO_BITRIX')
    resp.set_cookie('token', token)
    
    return resp
