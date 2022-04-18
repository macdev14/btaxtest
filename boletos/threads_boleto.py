import datetime, re

from threading import Thread
from boletos.serializers import BoletoSerializer

from tecnospeed import plugboletos
from boletos.models import Boleto, TemplateBoleto
from mongodb import querys
from core.models import Conta

def retorna_ultimo_nosso_numero(cedente_cpf_cnpj, cedente_conta_numero, cedente_conta_codigo_banco):
    obj = querys.get_first_obj(
        Boleto.COLLECTION_NAME,
        query={
            'cedente_cpf_cnpj': cedente_cpf_cnpj,
            'cedente_conta_numero': cedente_conta_numero,
            'cedente_conta_codigo_banco': cedente_conta_codigo_banco,
        },
        fields={'titulo_nosso_numero': 1},
        field_order='_id',
        desc=True,
    )

    return obj

class GeraBoletoThread(Thread):

    def __init__(self, cobranca):
        self.cobranca = cobranca
        Thread.__init__(self)

    def run(self):
        template_boleto = querys.get_obj_by_id(TemplateBoleto.COLLECTION_NAME, self.cobranca.template_boleto_id)
        print(self.cobranca.conta_id)
        cedente_cpf_cnpj = re.sub(r'[.\-/]', '', Conta.objects.values('cpf_cnpj').get(id=self.cobranca.conta_id)['cpf_cnpj'])
        print(cedente_cpf_cnpj)
        ultimo_nosso_numero = retorna_ultimo_nosso_numero(
            cedente_cpf_cnpj,
            template_boleto['cedente_conta_numero'],
            template_boleto['cedente_conta_codigo_banco'],
        )
        
        boleto = Boleto(
            cedente_cpf_cnpj = cedente_cpf_cnpj,
            cedente_conta_numero = template_boleto['cedente_conta_numero'],
            cedente_conta_numero_dv = template_boleto['cedente_conta_numero_dv'],
            cedente_conta_codigo_banco = template_boleto['cedente_conta_codigo_banco'],
            cedente_convenio_numero = template_boleto['cedente_convenio_numero'],
            sacado_cpf_cnpj = self.cobranca.sacado_cpf_cnpj,
            sacado_email = self.cobranca.sacado_email,
            sacado_endereco_numero = self.cobranca.sacado_endereco_numero,
            sacado_endereco_bairro = self.cobranca.sacado_endereco_bairro,
            sacado_endereco_cep = self.cobranca.sacado_endereco_cep,
            sacado_endereco_cidade = self.cobranca.sacado_endereco_cidade,
            sacado_endereco_complemento = self.cobranca.sacado_endereco_complemento,
            sacado_endereco_logradouro = self.cobranca.sacado_endereco_logradouro,
            sacado_endereco_pais = self.cobranca.sacado_endereco_pais,
            sacado_endereco_uf = self.cobranca.sacado_endereco_uf,
            sacado_nome = self.cobranca.sacado_nome,
            sacado_telefone = self.cobranca.sacado_telefone,
            sacado_celular = self.cobranca.sacado_celular,
            titulo_data_emissao = datetime.date.today().strftime('%d/%m/%Y'),
            titulo_data_vencimento = self.cobranca.titulo_data_vencimento,
            titulo_mensagem01 = template_boleto['titulo_mensagem01'],
            titulo_mensagem02 = template_boleto['titulo_mensagem02'],
            titulo_mensagem03 = template_boleto['titulo_mensagem03'],
            titulo_nosso_numero = int(ultimo_nosso_numero['titulo_nosso_numero']) + 1 if ultimo_nosso_numero else 1,
            titulo_numero_documento = self.cobranca.titulo_numero_documento,
            titulo_valor = self.cobranca.titulo_valor,
            titulo_local_pagamento = template_boleto['titulo_local_pagamento'],
            cobranca_id = self.cobranca._id
        )
        boleto.save()
        boleto_dict = boleto.dict_data()
        resposta = plugboletos.inclusao_boleto(**{k: boleto_dict[k] for k in boleto_dict.keys() if not k in ['cobranca_id', 'id_integracao', '_id', 'mensagem_falha']})
        print(resposta)
        if resposta['_status'] == 'sucesso':
            if len(resposta['_dados']['_sucesso']) > 0:
                boleto.situacao = getattr(boleto, resposta['_dados']['_sucesso'][0]['situacao'])
                boleto.id_integracao = resposta['_dados']['_sucesso'][0]['idintegracao']
                boleto.save()
            elif len(resposta['_dados']['_falha']) > 0:
                boleto.situacao = Boleto.FALHA
                boleto.save()
                return resposta
        else:
            
            print('Erro')
