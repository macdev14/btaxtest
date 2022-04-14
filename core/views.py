import json
from time import sleep
from bson.objectid import ObjectId

from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from boletos.models import TemplateBoleto
from rest_framework.authtoken.models import Token
import requests
from autenticacao.models import User
from autenticacao import gerador_senha
from .models import Conta, Profile, Telefone, Empresa
from .forms import ContasForm, EmpresaForm, EnderecoForm, TelefoneForm
from .forms import ServicoForm
from .decorators import only_administrators
from .envia_email import EnviaEmail

from mongodb import querys
from .models_mongodb import ServicoMongo, mongo_to_dict

from pybitrix24 import Bitrix24
from pybitrix import PyBitrix


 
# Local: 
# bx24 = Bitrix24('beytrix.bitrix24.com.br', 'local.625425573ccf01.19175085', 'QLwJT6k15YjxJX085UWCOFaqrs4JrQaNKnhhmtu3M3Djg2klcy' )
# auth_hostname="oauth.bitrix.info"
# https://beytrix.bitrix24.com.br/oauth/authorize/?client_id=local.625425573ccf01.19175085&response_type=code
# http://localhost:8000/?code=0c275462005ad5dd001942f700000318a0ab0798e2b501426e7cd42c5bf6a01bd507e3&state=&domain=beytrix.bitrix24.com.br&member_id=a6356c8a1ad614323f514888ad4f6068&scope=crm&server_domain=oauth.bitrix.info


# Local: client_secret= "QLwJT6k15YjxJX085UWCOFaqrs4JrQaNKnhhmtu3M3Djg2klcy"
#Local: client_id = "local.625425573ccf01.19175085"

# remoto:
client_id = "local.62542020d85557.44615100"

client_secret = "8MlsoRMTipPgHzU5ejSfGC6WZWxGm8Cik7nSHaBsLL1V5syQ2r"

domain = 'beytrix.bitrix24.com.br'

#remoto:
bx24 = Bitrix24(domain, client_id, client_secret)
print(bx24.build_authorization_url())
#auth_id = "0c275462005ad5dd001942f700000318a0ab0798e2b501426e7cd42c5bf6a01bd507e3"

data = None
app_id = client_id
app_secret = client_secret
b24  = None 
refresh_token = None
access_token = None
code = None
auth_url = bx24.build_authorization_url()

# ao instalar criar conta no btax -> enviar credenciais para o email de quem instalou

# gerar token adicionar no robot

def test_call(account_id):
    global b24, bx24, refresh_token
    print("Inside token: "+str(refresh_token))
    templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(account_id), 'deletado': False })

 #{"HANDLER_URL": "http://localhost:8000/api/cobrancas/emitir/"}
    bx24.call('bizproc.robot.delete', {'CODE': 'btax' })
    add_robo = bx24.call('bizproc.robot.add', {


        'CODE': 'btax',
        'HANDLER': 'https://dev.btax24.com/api/cobrancas/emitir/',
        'AUTH_USER_ID': '8da64525cfdfa028e0ae651dc41976a29526e6cd',
        'NAME': 'Btax',

        'PROPERTIES':{
           
              'template_boleto_id': {
                    'Name': 'Template de Boleto Cadastrado',
                    'Type': 'select',
                    'Options': {
                        '618315f0358ffd0721aeaebd': 'Template 1',
                        '': 'Template 2'
                    },
                    'Default': '618315f0358ffd0721aeaebd'
                },

                'sacado_cpf_cnpj': {
                    'Name': 'CPF ou CNPJ do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{sacado cpf cnpj}}'
                },

                 'sacado_email': {
                    'Name': 'E-mail do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{sacado email}}'
                },

                 'sacado_endereco_logradouro': {
                    'Name': 'Logradouro do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{endereço logradouro}}'
                },

                'sacado_endereco_numero': {
                    'Name': 'Número do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{Numero do Endereço do Sacado}}'
                },

                'sacado_endereco_complemento': {
                    'Name': 'Complemento do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{Complemento de Endereço do Sacado}}'
                },

                'sacado_endereco_cep': {
                    'Name': 'CEP do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{CEP do Endereço do Sacado}}'
                },

                'sacado_endereco_cidade': {
                    'Name': 'Cidade do endereço do Sacado',
                    'Type': 'string',
                    #Default': ''
                    'Default': '{{Cidade do Endereço do Sacado}}'
                },

                'sacado_endereco_uf': {
                    'Name': 'UF do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{UF do Endereço do Sacado}}'
                },

                 'sacado_endereco_pais': {
                    'Name': 'País do endereço do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{Pais do Endereço do Sacado}}'
                },


                 'sacado_nome': {
                    'Name': 'Nome do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{Nome do Sacado}}'
                },

                'sacado_telefone': {
                    'Name': 'Telefone do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{Telefone do Sacado}}'
                },

                'sacado_celular': {
                    'Name': 'Celular do Sacado',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{Celular do Sacado}}'
                },

                 'titulo_valor': {
                    'Name': 'Valor do título',
                    'Type': 'double',
                    #'Default': ''
                    'Default': '{{Valor}}'
                },

                'titulo_numero_documento': {
                    'Name': 'Valor para controle interno',
                    'Description': 'Campo que pode ser informado com um valor para controle interno.',
                    'Type': 'string',
                    #'Default': ''
                    'Default': '{{numero documento}}'
                },

                'titulo_data_vencimento': {
                    'Name': 'Data de vencimento do título ',
                    'Description': 'Data de vencimento do título no formato dd/mm/aaaa.',
                    'Type': 'date',
                    #'Default': ''
                    'Default': '{{data vencimento}}'
                },    
            
              
                
        },    
                
                
                #  '': {
                #     'Name': 'sacado_cpf_cnpj',
                #     'Type': 'string',
                #     'Default': ''
                #     #'Default': '{{sacado cpf cnpj}}'
                # },


           

            'RETURN_PROPERTIES': {
                'string': {
                    'Name': 'template_boleto_id',
                    'Type': 'string',
                    'Default': '618315f0358ffd0721aeaebd'
                },

                'string': {
                    'Name': 'sacado_cpf_cnpj',
                    'Type': 'string',
                    'Default': ''
                    #'Default': '{{sacado cpf cnpj}}'
                },

                 'string': {
                    'Name': 'sacado_email',
                    'Type': 'string',
                    'Default': ''
                    #'Default': '{{sacado email}}'
                },

                 'string': {
                    'Name': 'sacado_endereco_logradouro',
                    'Type': 'string',
                    'Default': ''
                    #'Default': '{{endereço logradouro}}'
                },

                'string': {
                    'Name': 'sacado_endereco_numero',
                    'Type': 'string',
                    'Default': ''
                    #'Default': '{{Numero do Endereço do Sacado}}'
                },

                'string': {
                    'Name': 'sacado_endereco_complemento',
                    'Type': 'string',
                    'Default': ''
                    #'Default': '{{Complemento de Endereço do Sacado}}'
                },

                'string': {
                    'Name': 'sacado_endereco_cep',
                    'Type': 'string',
                    'Default': ''
                    #'Default': '{{CEP do Endereço do Sacado}}'
                },

                'string': {
                    'Name': 'sacado_endereco_cidade',
                    'Type': 'string',
                    'Default': '',
                    'Default': '{{Cidade do Endereço do Sacado}}'
                },

                'string': {
                    'Name': 'sacado_endereco_uf',
                    'Type': 'string',
                    'Default': '',
                    #'Default': '{{UF do Endereço do Sacado}}'
                },

                 'string': {
                    'Name': 'sacado_endereco_pais',
                    'Type': 'string',
                    'Default': '',
                    #'Default': '{{Pais do Endereço do Sacado}}'
                },


                 'string': {
                    'Name': 'sacado_nome',
                    'Type': 'string',
                    'Default': '',
                    #'Default': '{{Nome do Sacado}}'
                },

                'string': {
                    'Name': 'sacado_telefone',
                    'Type': 'string',
                    'Default': '',
                    #'Default': '{{Telefone do Sacado}}'
                },

                'string': {
                    'Name': 'sacado_celular',
                    'Type': 'string',
                    'Default': '',
                    #'Default': '{{Celular do Sacado}}'
                },

                 'double': {
                    'Name': 'titulo_valor',
                    'Type': 'double',
                    'Default': '',
                    #'Default': '{{Valor}}'
                },

                'string': {
                    'Name': 'titulo_numero_documento',
                    'Type': 'string',
                    'Default': '',
                    #'Default': '{{numero documento}}'
                },

                'date': {
                    'Name': 'titulo_data_vencimento',
                    'Type': 'date',
                    'Default': ''
                    #'Default': '{{data vencimento}}'
                },




            }

            # 'PROPERTIES': {
            #     'bool': {
            #         'Name': 'Yes/No',
            #         'Type': 'bool',
            #         'Required': 'Y',
            #         'Multiple': 'N'
            #     },
            #     'date': {
            #         'Name': 'Date',
            #         'Type': 'date'
            #     },
            #     'datetime': {
            #         'Name': 'Date/Time',
            #         'Type': 'datetime'
            #     },
            #     'double': {
            #         'Name': 'Number',
            #         'Type': 'double',
            #         'Required': 'Y'
            #     },
            #     'int': {
            #         'Name': 'Integer number',
            #         'Type': 'int'
            #     },
            #     'select': {
            #         'Name': 'List',
            #         'Type': 'select',
            #         'Options': {
            #             'one': 'one',
            #             'two': 'two'
            #         }
            #     },
            #     'string': {
            #         'Name': 'String',
            #         'Type': 'string',
            #         'Default': 'default string value'
            #     },
            #     'text': {
            #         'Name': 'Text',
            #         'Type': 'text'
            #     },
            #     'user': {
            #         'Name': 'User',
            #         'Type': 'user'
            #     }
            # }

    }
    
    )
    #test = bx24.call_event_unbind('onCrmInvoiceAdd', 'http://btaxtest.herokuapp.com/api/cobrancas/emitir/', {'Authorization': 'Token dc188af8fb2ae310412bd58c2abc938ddc259ff5'})
    #test = bx24.call_event_bind('onCrmInvoiceAdd', 'http://btaxtest.herokuapp.com/api/cobrancas/emitir/', {'Authorization': 'Token dc188af8fb2ae310412bd58c2abc938ddc259ff5'})
    print("Event bind")
    #test = bx24.call_event_bind('OnAppUpdate', 'https://example.com/')
    #bx24.refresh_tokens()
    #b24 = PyBitrix(domain=domain, access_token=access_token, refresh_token=refresh_token, app_id=app_id, app_secret=app_secret)
    # test= b24.call('crm.invoice.list', {
    # 'order': ['DSC'],
       
    # })
    #print(test)
    print("Robot")
    print(add_robo)
    tst = bx24.call('bizproc.robot.list')
    print(tst)



@login_required
def home(request):
    global refresh_token, access_token, code, auth_url, bx24
   
    if request.method == "GET":
        if "code" in request.GET:
            code = request.GET["code"]
            #url = f"https://beytrix.bitrix24.com.br/oauth/token/?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}"
            #resp = requests.get(url=url)
            #data = resp.json()
            #print(data)
            # if resp.status_code == 200:
            #     refresh_token = data['refresh_token']
            #     access_token = data['access_token']
            #     #test_call()
        if (refresh_token is None) and  (access_token is None) and (code is None): return redirect(auth_url)
        try:
            tokens = bx24.obtain_tokens(code)
            print(tokens)
            refresh_token = tokens['refresh_token']
            access_token = tokens['access_token']
        except:
            return redirect(auth_url)
        print(refresh_token or None)
        print(access_token or None)
        print(code or None )
        test_call(request.user.id)
        return render(request, 'core/home.html')

@login_required
@only_administrators
def contas(request):
    #print(bx24.obtain_tokens('AnAuthorizationCode'))
    contas = Conta.objects.filter(is_deletado=False)

    return render(request, 'core/contas.html', 
        {
            'contas': contas,
        }
    )


def instalacao_conta(request):
    if (refresh_token is None) and (access_token is None) and (code is None): return redirect(auth_url)
    post_data = {'name': 'Gladys'}
    #usuario = User.objects.create_user_for_customer(email=conta.contato_email, password=senha, first_name=conta.nome)

@login_required
@only_administrators
def contas_novo(request):
    if request.method == 'POST':
        print(request.POST)
        return HttpResponseRedirect(reverse('core:contas'))
        form = ContasForm(request.POST)
        if form.is_valid():
            conta = form.save()

            senha = gerador_senha.gera_senha(8)
            usuario = User.objects.create_user_for_customer(email=conta.contato_email, password=senha, first_name=conta.nome)
            
            Profile.objects.create(
                conta=conta,
                usuario=usuario,
                nome=conta.nome,
                telefone=conta.contato_telefone,
                is_principal=True,
            )

            EnviaEmail(conta.contato_email, usuario.id, conta.nome).start()

            return HttpResponseRedirect(reverse('core:contas'))
        else:
            print(form.errors )
    else:
        form = ContasForm()

    return render(request, 'core/contas-cadastro.html', 
        {
            'form': form,
        }
    )

@login_required
@only_administrators
def contas_editar(request, conta_id):
    conta = get_object_or_404(Conta, id=conta_id)
    if request.method == 'POST':
        form = ContasForm(request.POST, instance=conta)
        if form.is_valid():
            conta = form.save()

            return HttpResponseRedirect(reverse('core:contas'))
        else:
            print(form.errors)
    else:
        form = ContasForm(instance=conta)

    return render(request, 'core/contas-cadastro.html', 
        {
            'conta': conta,
            'form': form,
        }
    ) 

@login_required
@only_administrators
def contas_excluir(request, conta_id):
    data = {}
    conta = get_object_or_404(Conta, id=conta_id)
    conta.delete()
    contas = Conta.objects.filter(is_deletado=False)
    data['html_lista'] = render_to_string('core/contas-lista-conteudo.html', {'contas': contas}, request=request)
    return JsonResponse(data)

@login_required
@only_administrators
def contas_atualizar_token(request, conta_id):
    data = {}
    conta = get_object_or_404(Conta, id=conta_id)
    usuario = conta.profiles.first().usuario
    Token.objects.filter(user=usuario).delete()
    Token.objects.create(user=usuario)
    contas = Conta.objects.filter(is_deletado=False)
    data['html_lista'] = render_to_string('core/contas-lista-conteudo.html', {'contas': contas}, request=request)
    return JsonResponse(data)

@login_required
def empresas(request):
    empresas = request.user.profile.conta.empresas.filter(deletado=False)
    return render(request, 'core/cliente/empresas.html',
        {
            'empresas': empresas,
        }
    )

@login_required
def empresas_novo(request):
    TelefoneFormSet = modelformset_factory(Telefone, form=TelefoneForm, can_delete=True)
    NumeracaoFormSet = modelformset_factory(Numeracao, form=NumeracaoForm, can_delete=True)
    if request.method == 'POST':
        form_empresa = EmpresaForm(request.POST, prefix='empresa')
        form_endereco = EnderecoForm(request.POST, prefix='endereco')
        formset_telefone = TelefoneFormSet(request.POST, prefix='telefone')
        form_nfse = NfseForm(request.POST, prefix='nfse')
        form_config_nfse = ConfigNfseForm(request.POST, prefix='config_nfse')
        form_rps = RpsForm(request.POST, prefix='rps')
        form_prefeitura = PrefeituraForm(request.POST, prefix='prefeitura')
        formset_numeracao = NumeracaoFormSet(request.POST, prefix='numeracao')
        
        if (form_empresa.is_valid() and
                form_endereco.is_valid() and
                formset_telefone.is_valid() and 
                form_nfse.is_valid() and
                form_config_nfse.is_valid() and
                form_rps.is_valid() and
                form_prefeitura.is_valid() and
                formset_numeracao.is_valid()):
            empresa = form_empresa.save(commit=False)
            empresa.conta = request.user.profile.conta
            empresa.save()

            endereco = form_endereco.save(commit=False)
            endereco.empresa = empresa
            endereco.save()

            telefones = formset_telefone.save(commit=False)
            for telefone in telefones:
                telefone.empresa = empresa
                telefone.save()

            for obj in formset_telefone.deleted_objects:
                obj.delete()

            nfse = form_nfse.save(commit=False)
            nfse.empresa = empresa
            nfse.save()

            config_nfse = form_config_nfse.save(commit=False)
            config_nfse.nfse = nfse
            config_nfse.save()

            prefeitura = form_prefeitura.save(commit=False)
            prefeitura.config_nfse = config_nfse
            prefeitura.save()

            rps = form_rps.save(commit=False)
            rps.config_nfse = config_nfse
            rps.save()

            numeracoes = formset_numeracao.save(commit=False)
            for numeracao in numeracoes:
                numeracao.rps = rps
                numeracao.save()

            for obj in formset_numeracao.deleted_objects:
                obj.delete()

            return HttpResponseRedirect(reverse('core:empresas'))
        else:
            print('form_empresa errors', form_empresa.errors)
            print('form_endereco errors', form_endereco.errors)
            print('formset_telefone errors', formset_telefone.errors)
            print('form_nfse errors', form_nfse.errors)
            print('form_config_nfse errors', form_config_nfse.errors)
            print('form_rps errors', form_rps.errors)
            print('form_prefeitura errors', form_prefeitura.errors)
            print('formset_numeracao errors', formset_numeracao.errors)
    else:
        form_empresa = EmpresaForm(prefix='empresa')
        form_endereco = EnderecoForm(prefix='endereco')
        formset_telefone = TelefoneFormSet(prefix='telefone', queryset=Telefone.objects.none())
        form_nfse = NfseForm(prefix='nfse')
        form_config_nfse = ConfigNfseForm(prefix='config_nfse')
        form_rps = RpsForm(prefix='rps')
        form_prefeitura = PrefeituraForm(prefix='prefeitura')
        formset_numeracao = NumeracaoFormSet(prefix='numeracao', queryset=Numeracao.objects.none())

    return render(request, 'core/cliente/empresas-cadastro.html',
        {
            'form_empresa': form_empresa,
            'form_endereco': form_endereco,
            'formset_telefone': formset_telefone,
            'form_nfse': form_nfse,
            'form_config_nfse': form_config_nfse,
            'form_rps': form_rps,
            'form_prefeitura': form_prefeitura,
            'formset_numeracao': formset_numeracao,
        }
    )

@login_required
def empresas_editar(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, deletado=False, conta=request.user.profile.conta)

    TelefoneFormSet = modelformset_factory(Telefone, form=TelefoneForm, can_delete=True, extra=0 if empresa.telefones.count() > 0 else 1)
    NumeracaoFormSet = modelformset_factory(Numeracao, form=NumeracaoForm, can_delete=True, extra=0 if empresa.nfse.config.rps.numeracao.count() > 0 else 1)
    
    if request.method == 'POST':
        form_empresa = EmpresaForm(request.POST, instance=empresa, prefix='empresa')
        form_endereco = EnderecoForm(request.POST, instance=empresa.endereco, prefix='endereco')
        formset_telefone = TelefoneFormSet(request.POST, queryset=empresa.telefones.all(), prefix='telefone')
        form_nfse = NfseForm(request.POST, instance=empresa.nfse, prefix='nfse')
        form_config_nfse = ConfigNfseForm(request.POST, instance=empresa.nfse.config, prefix='config_nfse')
        form_rps = RpsForm(request.POST, instance=empresa.nfse.config.rps, prefix='rps')
        form_prefeitura = PrefeituraForm(request.POST, instance=empresa.nfse.config.prefeitura, prefix='prefeitura')
        formset_numeracao = NumeracaoFormSet(request.POST, queryset=empresa.nfse.config.rps.numeracao.all(), prefix='numeracao')
        
        if (form_empresa.is_valid() and
                form_endereco.is_valid() and
                formset_telefone.is_valid() and 
                form_nfse.is_valid() and
                form_config_nfse.is_valid() and
                form_rps.is_valid() and
                form_prefeitura.is_valid() and
                formset_numeracao.is_valid()):
            empresa = form_empresa.save(commit=False)
            empresa.conta = request.user.profile.conta
            empresa.save()

            endereco = form_endereco.save(commit=False)
            endereco.empresa = empresa
            endereco.save()

            telefones = formset_telefone.save(commit=False)
            for telefone in telefones:
                telefone.empresa = empresa
                telefone.save()

            for obj in formset_telefone.deleted_objects:
                obj.delete()

            nfse = form_nfse.save(commit=False)
            nfse.empresa = empresa
            nfse.save()

            config_nfse = form_config_nfse.save(commit=False)
            config_nfse.nfse = nfse
            config_nfse.save()

            prefeitura = form_prefeitura.save(commit=False)
            prefeitura.config_nfse = config_nfse
            prefeitura.save()

            rps = form_rps.save(commit=False)
            rps.config_nfse = config_nfse
            rps.save()

            numeracoes = formset_numeracao.save(commit=False)
            for numeracao in numeracoes:
                numeracao.rps = rps
                numeracao.save()

            for obj in formset_numeracao.deleted_objects:
                obj.delete()

            return HttpResponseRedirect(reverse('core:empresas'))
        else:
            print('form_empresa errors', form_empresa.errors)
            print('form_endereco errors', form_endereco.errors)
            print('formset_telefone errors', formset_telefone.errors)
            print('form_nfse errors', form_nfse.errors)
            print('form_config_nfse errors', form_config_nfse.errors)
            print('form_rps errors', form_rps.errors)
            print('form_prefeitura errors', form_prefeitura.errors)
            print('formset_numeracao errors', formset_numeracao.errors)
    else:
        form_empresa = EmpresaForm(instance=empresa, prefix='empresa')
        form_endereco = EnderecoForm(instance=empresa.endereco, prefix='endereco')
        formset_telefone = TelefoneFormSet(queryset=empresa.telefones.all(), prefix='telefone')
        form_nfse = NfseForm(instance=empresa.nfse, prefix='nfse')
        form_config_nfse = ConfigNfseForm(instance=empresa.nfse.config, prefix='config_nfse')
        form_rps = RpsForm(instance=empresa.nfse.config.rps, prefix='rps')
        form_prefeitura = PrefeituraForm(instance=empresa.nfse.config.prefeitura, prefix='prefeitura')
        formset_numeracao = NumeracaoFormSet(queryset=empresa.nfse.config.rps.numeracao.all(), prefix='numeracao')

    return render(request, 'core/cliente/empresas-cadastro.html',
        {
            'form_empresa': form_empresa,
            'form_endereco': form_endereco,
            'formset_telefone': formset_telefone,
            'form_nfse': form_nfse,
            'form_config_nfse': form_config_nfse,
            'form_rps': form_rps,
            'form_prefeitura': form_prefeitura,
            'formset_numeracao': formset_numeracao,
        }
    )

@login_required
def empresas_excluir(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id, deletado=False, conta=request.user.profile.conta)
    empresa.delete()
    empresa = Empresa.objects.filter(deletado=False, conta=request.user.profile.conta)
    data = {
        'html_lista': render_to_string('core/cliente/empresas-lista-conteudo.html', {'empresas': empresas}, request=request),
    }
    return JsonResponse(data)

@login_required
def servicos(request):
    servicos = querys.filtra_objs(collection_name='servicos', query={'conta_id': str(request.user.profile.conta.id)})
    
    return render(request, 'core/cliente/servicos.html',
        {
            'servicos': servicos,
        }
    )

@login_required
def servicos_novo(request):
    if request.method == 'POST':
        servico_form = ServicoForm(request.POST)

        if servico_form.is_valid():
            cleaned_data = servico_form.cleaned_data
            servico = ServicoMongo(**cleaned_data)
            servico_dict = servico.dict_to_mongo()
            servico_dict['conta_id'] = str(request.user.profile.conta.id)
            id = querys.inserir_obj('servicos', servico_dict)
            return HttpResponseRedirect(reverse('core:servicos'))
        else:
            print('error no servico_form', servico_form.errors, flush=True)
    else:
        servico_form= ServicoForm()

    return render(request, 'core/cliente/servicos-cadastro.html',
        {
            'servico_form': servico_form,
        }
    )

@login_required
def servicos_editar(request, servico_id):
    servico = querys.get_obj('servicos', {'_id': ObjectId(servico_id), 'conta_id': str(request.user.profile.conta.id)})
    if not servico:
        raise Http404
    if request.method == 'POST':
        servico_form = ServicoForm(request.POST)
        if servico_form.is_valid():
            cleaned_data = servico_form.cleaned_data
            servico = ServicoMongo(**cleaned_data)
            servico_dict = servico.dict_to_mongo()
            querys.update_obj('servicos', servico_id, servico_dict)
            return HttpResponseRedirect(reverse('core:servicos'))
        else:
            print('error no servico_form', servico_form.errors, flush=True)
    else:
        servico_form= ServicoForm(initial=mongo_to_dict(servico))

    return render(request, 'core/cliente/servicos-cadastro.html',
        {
            'servico': servico,
            'servico_form': servico_form,
        }
    )

@login_required
def servicos_excluir(request, servico_id):
    conta = request.user.profile.conta
    querys.delete_obj('servicos', {'_id': ObjectId(servico_id), 'conta_id': str(conta.id)})

    servicos = querys.filtra_objs('servicos', {'conta_id': str(conta.id)})
    data = {
        'html_lista': render_to_string('core/cliente/servicos-lista-conteudo.html', {'servicos': servicos}, request=request)
    }
    return JsonResponse(data)