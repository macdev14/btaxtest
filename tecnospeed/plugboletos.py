from asyncio import sleep
import os
from turtle import update
import requests
import boto3
import asyncio
from btax.settings import *
from btax.config import bx24, update_deal
from django.templatetags.static import static
CNPJ = os.environ['TS_CNPJ']
TOKEN = os.environ['TS_TOKEN']
URL = os.environ['TS_PLUGBOLETO_BASE_URL']


def consulta_boleto(cedente_cpf_cnpj, id_integracao):
    headers = {
        'Content-Type': 'application/json',
        'cnpj-sh': CNPJ,
        'token-sh': TOKEN,
        'cnpj-cedente': cedente_cpf_cnpj,
    }
    response = requests.get(f'{URL}/boletos', params={'idintegracao': id_integracao}, headers=headers)
    return response.json()



async def obter_pdf(cedente_cpf_cnpj, protocolo, id_integracao,id_negocio=0):
    headers = {
        'Content-Type': 'application/json',
        'cnpj-sh': CNPJ,
        'token-sh': TOKEN,
        'cnpj-cedente': cedente_cpf_cnpj,
    }
    print('protocolo: '+ str(protocolo))
    await asyncio.sleep(1)
    response = requests.get(f'{URL}/boletos/impressao/lote/{protocolo}', headers=headers)
    print(response.content)
    binary_data = response.content

    s3 = boto3.resource(
    's3',
    region_name='us-east-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
    BUCKET_NAME = 'btax'
    PREFIX = 'boletos/'
    url_boleto = static('assets/'+PREFIX+f'boleto_{id_integracao}.pdf')
    s3.Object(BUCKET_NAME, PREFIX + f'boleto_{id_integracao}.pdf').put(Body=binary_data)
    print('url do boleto:', str(url_boleto))
    print('id_negocio:', str(id_negocio))
    asyncio.run(update_deal(id_negocio,url_boleto))
    #update = bx24.call('crm.deal.update', { 'id': id_negocio,  'fields':{'UF_CRM_1643650856094': url_boleto }} )
    
    try:
        with open(f"static/assets/boletos/boleto_{id_integracao}.pdf", "wb") as f:
            f.write(response.content)
    except:
        pass
    
    return True



async def solicitar_pdf(cedente_cpf_cnpj, id_integracao, id_negocio):
    #print('test')
    headers = {
        'Content-Type': 'application/json',
        'cnpj-sh': CNPJ,
        'token-sh': TOKEN,
        'cnpj-cedente': cedente_cpf_cnpj,
    }
    params = {
        "TipoImpressao" : "0",
        "Boletos" : [
            id_integracao,
]
    }
    await asyncio.sleep(1)
    response = requests.post(f'{URL}/boletos/impressao/lote', json=params, headers=headers)
   
    resp_json = response.json()
    print(resp_json)    

    # if '_dados' in resp_json and resp_json['_dados']:
    #     while resp_json['_dados']['situacao'] == 'PROCESSANDO':
    #         #sleep(5)
    #         response = requests.post(f'{URL}/boletos/impressao/lote', json=params, headers=headers)
    #         resp_json = response.json()
    #         print(resp_json)

    try:
        protocolo = resp_json['_dados']['protocolo']
        return await obter_pdf(cedente_cpf_cnpj, protocolo, id_integracao, id_negocio)
         
        
    except Exception as e:
        print(e)
        print(resp_json['_mensagem'])
        return resp_json['_mensagem']
    # finally: 
    #     return resp_json['_status']


def cadastro_cedente(dados_cedente):
    cedente = {
        "CedenteRazaoSocial": dados_cedente['razao_social'],
        "CedenteNomeFantasia": dados_cedente['nome_fantasia'],
        "CedenteCPFCNPJ": dados_cedente['cpf_cnpj'],
        "CedenteEnderecoLogradouro": dados_cedente['endereco_logradouro'],
        "CedenteEnderecoNumero": dados_cedente['endereco_numero'],
        "CedenteEnderecoComplemento": dados_cedente['endereco_complemento'],
        "CedenteEnderecoBairro": dados_cedente['endereco_bairro'],
        "CedenteEnderecoCEP": dados_cedente['endereco_cep'],
        "CedenteEnderecoCidadeIBGE": dados_cedente['endereco_cidade_ibge'],
        "CedenteTelefone": dados_cedente['endereco_telefone'],
        "CedenteEmail": dados_cedente['endereco_email']
    }

    headers = {
        'Content-Type': 'application/json',
        'cnpj-sh': CNPJ,
        'token-sh': TOKEN,
    }
    response = requests.post(f'{URL}cedentes/', json=cedente, headers=headers)
    return response.json()

def inclusao_boleto(cedente_cpf_cnpj, cedente_conta_numero, cedente_conta_numero_dv, cedente_convenio_numero, cedente_conta_codigo_banco, sacado_cpf_cnpj,
        sacado_email, sacado_endereco_numero, sacado_endereco_bairro, sacado_endereco_cep, sacado_endereco_cidade, sacado_endereco_complemento,
        sacado_endereco_logradouro, sacado_endereco_pais, sacado_endereco_uf,sacado_nome, sacado_telefone, sacado_celular, titulo_data_emissao,
        titulo_data_vencimento, titulo_mensagem01, titulo_mensagem02, titulo_mensagem03, titulo_nosso_numero, titulo_numero_documento,
        titulo_valor, titulo_local_pagamento):
    boleto = [
        {
            "CedenteContaNumero": cedente_conta_numero,
            "CedenteContaNumeroDV": cedente_conta_numero_dv,
            "CedenteConvenioNumero": cedente_convenio_numero,
            "CedenteContaCodigoBanco": cedente_conta_codigo_banco,
            "SacadoCPFCNPJ": sacado_cpf_cnpj,
            "SacadoEmail": sacado_email,
            "SacadoEnderecoNumero": sacado_endereco_numero,
            "SacadoEnderecoBairro": sacado_endereco_bairro,
            "SacadoEnderecoCEP": sacado_endereco_cep,
            "SacadoEnderecoCidade": sacado_endereco_cidade,
            "SacadoEnderecoComplemento": sacado_endereco_complemento,
            "SacadoEnderecoLogradouro": sacado_endereco_logradouro,
            "SacadoEnderecoPais": sacado_endereco_pais,
            "SacadoEnderecoUF": sacado_endereco_uf,
            "SacadoNome": sacado_nome,
            "SacadoTelefone": sacado_telefone,
            "SacadoCelular": sacado_celular,
            "TituloDataEmissao": titulo_data_emissao,
            "TituloDataVencimento": titulo_data_vencimento,
            "TituloMensagem01": titulo_mensagem01,
            "TituloMensagem02": titulo_mensagem02,
            "TituloMensagem03": titulo_mensagem03,
            "TituloNossoNumero": titulo_nosso_numero,
            "TituloNumeroDocumento": titulo_numero_documento,
            "TituloValor": titulo_valor,
            "TituloLocalPagamento": titulo_local_pagamento,
        }
    ]

    headers = {
        'Content-Type': 'application/json',
        'cnpj-sh': CNPJ,
        'token-sh': TOKEN,
        'cnpj-cedente': cedente_cpf_cnpj,
    }

    response = requests.post(f'{URL}/boletos/lote', json=boleto, headers=headers)
    resposta = response.json()
    try:
        # sleep(0.5)
        # print('ran') 
        id_integracao = resposta['_dados']['_sucesso'][0]['idintegracao']
        asyncio.run(solicitar_pdf(cedente_cpf_cnpj, id_integracao, titulo_numero_documento))
        
    except Exception as e:
        print(e)
    return response.json()






