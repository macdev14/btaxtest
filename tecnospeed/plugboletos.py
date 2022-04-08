import os
import requests

CNPJ = os.environ['TS_CNPJ']
TOKEN = os.environ['TS_TOKEN']
URL = os.environ['TS_PLUGBOLETO_BASE_URL']

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

    return response.json()

def consulta_boleto(cedente_cpf_cnpj, id_integracao):
    headers = {
        'Content-Type': 'application/json',
        'cnpj-sh': CNPJ,
        'token-sh': TOKEN,
        'cnpj-cedente': cedente_cpf_cnpj,
    }
    response = requests.get(f'{URL}/boletos', params={'idintegracao': id_integracao}, headers=headers)
    return response.json()