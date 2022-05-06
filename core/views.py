import json, urllib
from wsgiref import headers
from bson.objectid import ObjectId

from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.forms import modelformset_factory
from unidecode import unidecode
from rest_framework.authtoken.models import Token
from urllib.parse import unquote
from autenticacao.models import User
from autenticacao import gerador_senha
from .models import Conta, Profile, Telefone, Empresa
from .forms import ContasForm, EmpresaForm, EnderecoForm, TelefoneForm
from .forms import ServicoForm
from .decorators import only_administrators
from .envia_email import EnviaEmail

from mongodb import querys
from .models_mongodb import ServicoMongo, mongo_to_dict
from boletos.models import TemplateBoleto
from bitrix24.bitrix24 import *
from pybitrix24 import Bitrix24
import schedule
from django.templatetags.static import static
from btax.settings import BITRIX_LOCAL, CLIENT_SECRET_LOCAL, CLIENT_ID_LOCAL, CLIENT_ID, CLIENT_SECRET, DOMAIN, TS_PLUGBOLETO_BASE_URL, TS_TOKEN, TS_CNPJ
from btax.decorators import bitrix_auth

#remoto:
bx24 = Bitrix24(DOMAIN, CLIENT_ID, CLIENT_SECRET)

#local:
if BITRIX_LOCAL:
    bx24 = Bitrix24(DOMAIN, CLIENT_ID_LOCAL, CLIENT_SECRET_LOCAL)


print(bx24.build_authorization_url())
#auth_id = "0c275462005ad5dd001942f700000318a0ab0798e2b501426e7cd42c5bf6a01bd507e3"





code, data, access_token, refresh_token = None, None, None, None

auth_url = bx24.build_authorization_url()
instalation = False

def set_tokens(dicts=[]):
    global access_token, refresh_token
    print(dicts)
    
    access_token = dicts['access_token']
    refresh_token = dicts['refresh_token']
    

def schedule_refresh():
    def sched_set():
        set_tokens(bx24.refresh_tokens())
    schedule.every(1).minutes.do(sched_set)

# gerar token adicionar no robot


#@bitrix_auth(bx24)
def instalacao_btax(request):
    # Obter variaveis globais para modificacao e leitura
    global refresh_token, access_token, code, auth_url, bx24, instalation
    instalation = True
    ''' 

    Autorizar app a obter informacoes de quem instalou o btax e voltar para a pagina de instalacao para criar o robot com o token 

    '''
    # se estiver vazio os tokens de acesso autorizar novamente e obter tokens 
    if (refresh_token is None) and (access_token is None) and (code is None): return redirect(auth_url)
    
    # obter informacoes do usuario caso nao haja redireciona para a pagina principal
    #if not 'result' in bx24.call('user.current'): return redirect('core:home')
    
    try:
        bitrix24_user = bx24.call('user.current')['result'] 
        bitrix24_user_tst = bx24.call('user.current')
        bitrix24_user_tst['result']
    except:
        return redirect('core:home')
    
    #print(bitrix24_user)
    
    info = bitrix24_user
    #print("info")

    #print(info)


        
    # guardar informacoes nome e email
    email = info["EMAIL"]
    nome = info["NAME"]+ " "+info["LAST_NAME"]

    # verificar se existe uma conta com este nome e email
    if Conta.objects.filter(contato_email=email).exists():
        # teste de obter conta; conta = Conta.objects.get(is_deletado=False, nome=nome,email=email)
       
        # obter usuario que possui este email
        user = User.objects.get(email=email)

        # obter token
        token = Token.objects.get(user=user)

        # passar token e id do usuario do btax para criacao do robo no bitrix24
        print("Creating Robot")
        
        instalation = False
        try:
            install_robot(token, user.profile.conta.id, bx24, info['ID'], request.META['HTTP_HOST'])
            return redirect(auth_url)
        except:
            return redirect(reverse('core:instalacao'))
        # resp = redirect('core:home')
        # resp.set_cookie('token', token)
        # return resp
    # Se não possuir conta no btax24 o usuário que tentou instalar será notificado
    print("Error while creating robot")
    bx24.call('im.notify', {'to': int(info['ID']), 'message': 'Conta com esse Email inexistente'  })
    instalation = False
    
    resp = redirect('core:home')
    #resp.set_cookie('token', token)
    return resp



def update_btax(request):
    # Obter variaveis globais para modificacao e leitura
    global refresh_token, access_token, code, auth_url, bx24, instalation
    instalation = False
    ''' 

    Autorizar app a obter informacoes de quem instalou o btax e voltar para a pagina de instalacao para criar o robot com o token 

    '''
    # se estiver vazio os tokens de acesso autorizar novamente e obter tokens 
    if (refresh_token is None) and (access_token is None) and (code is None): return redirect(auth_url)
    
    # obter informacoes do usuario caso nao haja redireciona para a pagina principal
    #if not 'result' in bx24.call('user.current'): return redirect('core:home')
    print("update called")
    
    
   
   

        
    
    
   
    try:
        # guardar informacoes: email
        bitrix24_user = bx24.call('user.current')['result'] 
        info = bitrix24_user
        email = info["EMAIL"]
        # verificar se existe uma conta com este nome e email
        if Conta.objects.filter(contato_email=email).exists():
        # teste de obter conta; conta = Conta.objects.get(is_deletado=False, nome=nome,email=email)
       
        # obter usuario que possui este email
            user = User.objects.get(email=email)

        # obter token
            token = Token.objects.get(user=user)

        # passar token e id do usuario do btax para criacao do robo no bitrix24
            print("Updating Robot View")
        
        
       
            update_robot(token, user.profile.conta.id, bx24, info['ID'], request.META['HTTP_HOST'])
            return redirect('boletos:templates')
    
        print("Error while updating robot")
        #bx24.call('im.notify', {'to': int(info['ID']), 'message': 'Conta com esse Email inexistente'  })
        if 'NOTIFICACAO_BITRIX' in request.COOKIES and request.COOKIES['NOTIFICACAO_BITRIX']:
            bx24.call('im.notify', {'to': int(info['ID']), 'message': request.COOKIES['NOTIFICACAO_BITRIX']  })
        if 'id_integracao' in request.COOKIES and request.COOKIES['id_integracao']:
            bx24.call('crm.deal.update', {'id': 4758, 'fields':{  "UF_CRM_1643650856094":  static(f'/boletos/boleto_{request.COOKIES["id_integracao"]}.pdf' )   }	  })
            
    except:
        resp = redirect('core:home')
        resp.set_cookie('VIEW_REDIRECT', 'core:update-btax')
        return resp
       
    # Se não possuir conta no btax24 o usuário que tentou instalar será notificado
    
    
    resp = redirect('boletos:templates')
    resp.delete_cookie('NOTIFICACAO_BITRIX')
    #resp.set_cookie('token', token)
    return resp



@login_required
def home(request,  url_name="", **kwargs):
    global refresh_token, access_token, code, auth_url, bx24, instalation
    
    print("kwargs: ")
    print(kwargs)
    print("url name: ")
    print(url_name)
    #if 'code' in request.GET:
    if 'code' in request.GET: code = request.GET['code'] 
    try: 
        bx24.obtain_tokens(code)['access_token'] if 'access_token' in bx24.obtain_tokens(code) else redirect(auth_url)
        bx24.refresh_tokens()
        print("inside kwargs: ")
        print(kwargs)
            # if kwargs.get('url_name'):
            #     print(url_name)
            #     #resp = kwargs.get('url_name')
            #     try: resp = redirect(reverse(url_name, args=[1]))
            #     except: resp = redirect(reverse(url_name, kwargs=kwargs))
            #     #bx24.refresh_tokens()
                
            #    return resp
           
        
        
    except Exception as e:
        print(e) 
        return redirect(auth_url)
        

    if instalation:
        instalation = False
        resp = redirect('core:instalacao')
                #bx24.refresh_tokens()
        resp.set_cookie('bitrix_code', code)
        return resp
        
    if 'VIEW_REDIRECT' in request.COOKIES and request.COOKIES['VIEW_REDIRECT']:
        try: resp = redirect(reverse(request.COOKIES['VIEW_REDIRECT'], args=[1]))
        except: resp = redirect(reverse(request.COOKIES['VIEW_REDIRECT'], kwargs=kwargs))
        resp.set_cookie('bitrix_code', code)
        resp.delete_cookie('VIEW_REDIRECT')
        return resp
        
        
    resp = render(request, 'core/home.html')
    resp.set_cookie('bitrix_code', code)
    return resp
    # try:

    #     templates_boletos = querys.filtra_objs(TemplateBoleto.COLLECTION_NAME, {'conta_id': str(request.user.profile.conta.id), 'deletado': False })
        
    #     dict_options = {}
    #     for id_boleto in templates_boletos:
    #         dict_options[ str(id_boleto.get('descricao')) ] = str(id_boleto.get('_id'))
    # except:
    #     pass 



    #print(dict_options)
    # def auth_redirect():
    #     return redirect(auth_url)
    
    # if request.method == "GET":
    #     if "code" in request.GET:
    #         code = request.GET["code"]
    #         if url_name:
    #             try: bx24.obtain_tokens(code)
    #             except:redirect(auth_url)
    #             resp = redirect(url_name)

    #             resp.set_cookie('bitrix_code', code)
                
    #             return resp
        #if (refresh_token is None) and  (access_token is None) and (code is None): return redirect(auth_url)
        # try:
        #     tokens = bx24.obtain_tokens(code)
        #     print(tokens)
        #     refresh_token = tokens['refresh_token']
        #     access_token = tokens['access_token']
        #     #bx24.call('bizproc.robot.delete', {'CODE': 'btax' })
            
        # except: 
        #     schedule.every(50).minutes.do(auth_redirect)
            
        #     return redirect(auth_url)
        # print(refresh_token or None)
        # print(access_token or None)
        # print(code or None )
        # print("instalacao: ")
        # print(instalation)
        # schedule_refresh()
        




        
        




@login_required
@only_administrators

def contas(request):
    contas = Conta.objects.filter(is_deletado=False)

    return render(request, 'core/contas.html', 
        {
            'contas': contas,
        }
    )

@login_required
@only_administrators
def contas_novo(request):
    if request.method == 'POST':
        data = request.POST
        ''' 
        print(request.POST['endereco_cidade'])
        
        print(dict(request.POST))
        url_man = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{municipio}'.format(municipio=data['endereco_cidade'].replace(' ','-'))
        url_mun = '' + unquote(url_man, encoding="latin-1")
        mun_resp = requests.get(unidecode(url_mun))
        print(mun_resp.url)
        print(mun_resp.json())
        d_id = mun_resp.json()['id']
        print(d_id)
            
        techno_url = TS_PLUGBOLETO_BASE_URL+'cedente'
        headers={'Content-Type': 'application/json', 'cnpj-sh': TS_CNPJ, 'token-sh': TS_TOKEN}
        params = {
                'CedenteRazaoSocial': str(data['nome']), 
                'CedenteCPFCNPJ': str(data['cpf_cnpj']), 
                'CedenteEnderecoLogradouro': str(data['endereco_logradouro']),
                'CedenteEnderecoNumero': str(data['endereco_numero']),
                'CedenteEnderecoComplemento': str(data['endereco_complemento']),
                'CedenteEnderecoBairro': str(data['endereco_bairro']),
                'CedenteEnderecoCEP': str(data['endereco_cep']),
                'CedenteEnderecoCidadeIBGE': d_id,
                'CedenteTelefone': str(data['contato_telefone']),
                'CedenteEmail': str(data['contato_email'])

            }
        cedente_post = requests.post(url=techno_url, headers=headers, params=params)
        print(cedente_post.json())
        data['id_cedente'] = cedente_post.json()['_dados']['id']
        '''



        form = ContasForm(data)
       
        #print(request.POST.json())



        #return print([ i for i in request.POST.items()])
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