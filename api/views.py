from http.client import HTTPResponse
import json, requests
from django.shortcuts import reverse, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

from bson.errors import InvalidId
from bson.objectid import ObjectId

from boletos.models import Boleto
from boletos.serializers import CobrancaSerializer
from boletos.threads_boleto import GeraBoletoThread
from mongodb import querys

from tecnospeed import plugboletos

from bitrix24 import bitrix24
from pybitrix24 import Bitrix24
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import datetime
import json
from django.http import JsonResponse
from btax.settings import CLIENT_ID, CLIENT_SECRET, DOMAIN
from btax.decorators import bitrix_auth
from btax.config import bx24
from django.templatetags.static import static
#remoto:


#local:
# if BITRIX_LOCAL:
#     bx24 = Bitrix24(DOMAIN, CLIENT_ID_LOCAL, CLIENT_SECRET_LOCAL)


@csrf_exempt
def token_redirect(request):

    ''' funcao para obter token e postar na url /emissao/cobranca '''
    
    if 'user_token' in request.GET:
        #  para verificar entrada
        print('TOKEN')
        print(request.GET['user_token'])
        print(request.POST.dict())

        bitrix_user = request.GET['bitrix_user'] if 'bitrix_user' in request.GET else None
        
        # para verificar id do usuario
        print("bitrix user id: "+ str(bitrix_user) )
        print("DATA: ")
        # criar payload e header
        payload = {}
        pst_rq = request.POST.dict()
        for key in pst_rq:
            print(key[key.find("[")+1:key.rfind("]")])
            # definir chaves retirar [] do string
            k = key[key.find("[")+1:key.rfind("]")]
            # print(":")
            # print(pst_rq[key])
            ''' se houver propriedades na chave original verificar se a chave nova eh data se for convertar data '''
            if 'properties' in key:
                if k == "titulo_data_vencimento" and pst_rq[key]:
                    date_time = datetime.datetime.strptime(pst_rq[key], "%d/%m/%Y").strftime('%Y-%m-%d')
                    payload[k] = date_time
                else:
                    payload[k] = pst_rq[key]
        
        # definir headers
        headers = {'Content-Type': 'application/json', 'Authorization': 'Token '+request.GET['user_token']}
        # mostrar headers
        print(headers)
        # mostrar payload
        print("PAYLOAD")
        print(payload)
        print(payload['titulo_numero_documento'])
        id_negocio =payload['titulo_numero_documento']
        PREFIX = 'boletos/'
        url_boleto_payload = static('assets/'+PREFIX+f'boleto_{id_negocio}.pdf')
        payload_boleto = {
            'id_negocio' : id_negocio,
            'url_boleto': url_boleto_payload
        }
        
        # gerar url p/ requisicao
        url = request.build_absolute_uri(reverse('api:cobrancas-emitir'))
        print(url)

        url_boleto = request.build_absolute_uri(reverse('core:boleto-url-update'))
        print(url_boleto)

        # realizar requisicao
        r = requests.post(url, data=json.dumps(payload), headers=headers)
        print("JSON RESPONSE")
        boleto_ = requests.post(url_boleto, data=json.dumps(payload_boleto), headers=headers)
        # mostrar resposta
        print(r.json())
        new = r.json()
        obj = {}
       


        obj["properties[id]"] = new['id']
        # retornar resposta
        json_obj = json.dumps(obj)
        json_obj = json.loads(json_obj)
        print("object json: ")
        print(json_obj)
        #return JsonResponse(json_obj)
        return redirect(reverse('boleto-url-update', kwargs=payload_boleto))
        #response = dict(r.json())
        # if not "id" in response:   
        #     bx24.call('im.notify', {'to': int(bitrix_user), 'message': 'Conta com esse Email inexistente'  })

        #data_response['message'] = 'Testando..'
        #status_code = status_code = status.HTTP_200_OK
        return redirect(reverse('core:home'))
   

class TesteList(APIView):
    # permisson_classes = [IsAuthenticated, TokenHasScope]
    def get(self, format=None):
        lista = [
            {
                'nome': 'Joao henrique',
                'idade': 34
            },
            {
                'nome': 'Andréa',
                'idade': 38
            },
            {
                'nome': 'Théo',
                'idade': 3
            },
        ]

        return Response(lista)

class CobrancaEmitir(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        print('DATA:', flush=True)
        print(request.data, flush=True)
        print('HEADERS', flush=True)
        print(request.headers, flush=True)
        print('DICT', flush=True)
        print(request.__dict__, flush=True)
        print('GET', flush=True)
        print(request.__dict__, flush=True)
        print('POST', flush=True)
        print(request.__dict__, flush=True)
        print(request.__dict__)
        serializer = CobrancaSerializer(conta=request.user.profile.conta, data=request.data)
        if serializer.is_valid():
            cobranca = serializer.save()
            cobranca.save()
            GeraBoletoThread(cobranca).start()
            
            return Response(
                {
                    'id': str(cobranca._id)
                },
                status=status.HTTP_201_CREATED,
            )
        
        # gerar notificacao
        errors = "Campos incorretos: " #+ str([ str(i+' ') for i in serializer.errors.values() ] )
        print("Follow errors!!!!")
        print(serializer.errors.values())
       
        
     
        resp = Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        resp.set_cookie('NOTIFICACAO_BITRIX', errors)
        return resp
        return Response({'mensagem': 'requisição recebida'})

class CobrancaConsulta(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        cobranca_id = request.GET.get('cobranca_id')
        data_response = {}
        status_code = status.HTTP_200_OK
        if cobranca_id:
            try:
                resposta = querys.get_obj(
                    Boleto.COLLECTION_NAME,
                    {
                        'cobranca_id': ObjectId(cobranca_id)
                    },
                    fields=[
                        '_id',
                        'cobranca_id',
                        'situacao',
                        'cedente_cpf_cnpj',
                        'id_integracao',
                    ]
                )
                if resposta:
                    dados_boleto = plugboletos.consulta_boleto(resposta['cedente_cpf_cnpj'], resposta['id_integracao']) 
                    data_response['cobranca_id'] = str(resposta['cobranca_id'])
                    data_response['boleto_id'] = str(resposta['_id'])
                    data_response['situacao'] = resposta['situacao']
                    data_response['boleto_url'] = dados_boleto['_dados'][0]['UrlBoleto']
                    data_response['boleto_linha_digitavel'] = dados_boleto['_dados'][0]['TituloLinhaDigitavel']
                    data_response['boleto_codigo_barras'] = dados_boleto['_dados'][0]['TituloCodigoBarras']
                else:
                    data_response['message'] = 'Cobrança não encontrada'
                    status_code = status.HTTP_400_BAD_REQUEST
            except InvalidId:
                data_response['message'] = 'id inválido'
                status_code = status.HTTP_400_BAD_REQUEST
        else:
            data_response['message'] = 'informe o id da cobrança'
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data_response, status=status_code)
    
class BoletoRecebeNotificacao(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        
        data = request.data
        if 'notifica_registrou' in data['tipoWH']:
            boleto = querys.get_obj(Boleto.COLLECTION_NAME, {'id_integracao': data['titulo']['idintegracao']})
            boleto_pb = plugboletos.consulta_boleto(boleto['cedente_cpf_cnpj'], boleto['id_integracao'])
            print(boleto_pb)
            boleto['boleto_url'] = boleto_pb['_dados'][0]['UrlBoleto']
            boleto['situacao'] = boleto_pb['_dados'][0]['situacao']
            querys.update_obj(Boleto.COLLECTION_NAME, boleto['_id'], boleto)


        elif 'notifica_liquidou' in data['tipoWH']:
            boleto = querys.get_obj(Boleto.COLLECTION_NAME, {'id_integracao': data['titulo']['idintegracao']})
            boleto_pb = plugboletos.consulta_boleto(boleto['cedente_cpf_cnpj'], boleto['id_integracao'])
            boleto['situacao'] = boleto_pb['_dados'][0]['situacao']
            boleto['pagamento_data'] = data['titulo']['PagamentoData']
            boleto['pagamento_valor_pago'] = data['titulo']['PagamentoValorPago']
            boleto['pagamento_data_credito'] = data['titulo']['PagamentoDataCredito']
            querys.update_obj(Boleto.COLLECTION_NAME, boleto['_id'], boleto)

        elif data['tipoWH'] in ['notifica_baixou', 'notifica_rejeitou', 'notifica_alterou']:
            boleto = querys.get_obj(Boleto.COLLECTION_NAME, {'id_integracao': data['titulo']['idintegracao']})
            boleto_pb = plugboletos.consulta_boleto(boleto['cedente_cpf_cnpj'], boleto['id_integracao'])
            boleto['situacao'] = boleto_pb['_dados'][0]['situacao']
            querys.update_obj(Boleto.COLLECTION_NAME, boleto['_id'], boleto)

        return Response(status=status.HTTP_200_OK)