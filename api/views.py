import json, requests
from django.shortcuts import reverse
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





@csrf_exempt
def token_redirect(request):
    if 'user_token' in request.GET:
        print('TOKEN')
        print(request.GET['user_token'])
        #print(request.POST.dict())
        print("DATA: ")
        payload = {}
        pst_rq = request.POST.dict()
        for key in pst_rq:
            print(key[key.find("[")+1:key.rfind("]")])
            k = key[key.find("[")+1:key.rfind("]")]
            print(":")
            print(pst_rq[key])
            if 'properties' in key:
                payload[k] = pst_rq[key]
        headers = {'Content-Type': 'application/json', 'Authorization': 'Token '+request.GET['user_token']}
        print(headers)
        print("PAYLOAD!!!!")
        print(payload)
        url = request.build_absolute_uri(reverse('api:cobrancas-emitir'))
        print(url)
        requests.post(url, data=json.dumps(payload), headers=headers)
   

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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
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