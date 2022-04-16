import datetime
from uuid import UUID
from decimal import Decimal

from mongodb import querys

class Base():
    def dict_data(self):
        data = {}
        for k in self.__dict__.keys():
            if k[:2] != '__' and k.islower():
                if isinstance(self.__dict__[k], datetime.date):
                    data[k] = self.__dict__[k].strftime('%d/%m/%Y')
                elif isinstance(self.__dict__[k], float):
                    data[k] = f'{self.__dict__[k]:.2f}'.replace('.', ',')
                else:
                    data[k] = self.__dict__[k]
        return data

    def save(self):
        if hasattr(self, '_id'):
            querys.update_obj(self.COLLECTION_NAME, self._id, self.dict_data())
        else:
            id = querys.inserir_obj(self.COLLECTION_NAME, self.dict_data())
            self._id = id
        return self

class Boleto(Base):
    
    COLLECTION_NAME = 'boletos'

    SALVO = 'SALVO'
    FALHA = 'FALHA'
    EMITIDO = 'EMITIDO'
    REJEITADO = 'REJEITADO'
    REGISTRADO = 'REGISTRADO'
    LIQUIDADO = 'LIQUIDADO'
    BAIXADO = 'BAIXADO'
    PENDENTE_RETENTATIVA = 'PENDENTE_RETENTATIVA'
    SITUACOES = (
        (SALVO, 'Salvo'),
        (FALHA, 'Falha'),
        (EMITIDO, 'Emitido'),
        (REJEITADO, 'Rejeitado'),
        (REGISTRADO, 'Registrado'),
        (LIQUIDADO, 'Liquidado'),
        (BAIXADO, 'Baixado'),
        (PENDENTE_RETENTATIVA, 'Pendente - Retentativa'),
    )

    def __init__(self, cedente_cpf_cnpj, cedente_conta_numero, cedente_conta_numero_dv, cedente_conta_codigo_banco, cedente_convenio_numero,
        sacado_cpf_cnpj, sacado_email, sacado_endereco_numero, sacado_endereco_bairro, sacado_endereco_cep, sacado_endereco_cidade,
        sacado_endereco_complemento, sacado_endereco_logradouro, sacado_endereco_pais, sacado_endereco_uf, sacado_nome, sacado_telefone,
        sacado_celular, titulo_data_emissao, titulo_data_vencimento, titulo_mensagem01, titulo_mensagem02, titulo_mensagem03,
        titulo_nosso_numero, titulo_numero_documento, titulo_valor, titulo_local_pagamento, cobranca_id, id_integracao=None, _id=None,
        mensagem_falha=''):
        self.cedente_cpf_cnpj = cedente_cpf_cnpj
        self.cedente_conta_numero = cedente_conta_numero
        self.cedente_conta_numero_dv = cedente_conta_numero_dv
        self.cedente_conta_codigo_banco = cedente_conta_codigo_banco
        self.cedente_convenio_numero = cedente_convenio_numero
        self.sacado_cpf_cnpj = sacado_cpf_cnpj
        self.sacado_email = sacado_email
        self.sacado_endereco_numero = sacado_endereco_numero
        self.sacado_endereco_bairro = sacado_endereco_bairro
        self.sacado_endereco_cep = sacado_endereco_cep
        self.sacado_endereco_cidade = sacado_endereco_cidade
        self.sacado_endereco_complemento = sacado_endereco_complemento
        self.sacado_endereco_logradouro = sacado_endereco_logradouro
        self.sacado_endereco_pais = sacado_endereco_pais
        self.sacado_endereco_uf = sacado_endereco_uf
        self.sacado_nome = sacado_nome
        self.sacado_telefone = sacado_telefone
        self.sacado_celular = sacado_celular
        self.titulo_data_emissao = titulo_data_emissao
        self.titulo_data_vencimento = titulo_data_vencimento
        self.titulo_mensagem01 = titulo_mensagem01
        self.titulo_mensagem02 = titulo_mensagem02
        self.titulo_mensagem03 = titulo_mensagem03
        self.titulo_nosso_numero = titulo_nosso_numero
        self.titulo_numero_documento = titulo_numero_documento
        self.titulo_valor = titulo_valor
        self.titulo_local_pagamento = titulo_local_pagamento
        self.cobranca_id = cobranca_id
        self.mensagem_falha = mensagem_falha
        if _id:
            self._id = _id
        if id_integracao:
            self.id_integracao = id_integracao

class TemplateBoleto(Base):
    COLLECTION_NAME = 'templates_boletos'

    def __init__(self, conta_id, descricao, cedente_conta_codigo_banco, cedente_conta_numero, cedente_conta_numero_dv,
        cedente_convenio_numero, titulo_aceite, titulo_doc_especie, titulo_local_pagamento, titulo_cod_desconto,
        titulo_prazo_desconto, titulo_valor_desconto_taxa, titulo_cod_desconto2, titulo_prazo_desconto2,
        titulo_valor_desconto_taxa2, titulo_codigo_juros, titulo_prazo_juros, titulo_valor_juros, titulo_codigo_multa,
        titulo_prazo_multa, titulo_valor_multa_taxa, titulo_cod_protesto, titulo_prazo_protesto, titulo_cod_baixa_devolucao,
        titulo_prazo_baixa, titulo_mensagem01, titulo_mensagem02, titulo_mensagem03, titulo_sacador_avalista,
        titulo_sacador_avalista_endereco, titulo_sacador_avalista_cidade, titulo_sacador_avalista_cep, titulo_sacador_avalista_uf,
        titulo_inscricao_sacador_avalista, titulo_emissao_boleto, titulo_categoria, titulo_postagem_boleto, titulo_cod_emissao_bloqueto,
        titulo_outros_acrescimos, titulo_informacoes_adicionais, titulo_instrucoes, titulo_variacao_carteira, deletado=False, _id=None):

        self.descricao = descricao
        self.conta_id = conta_id
        self.cedente_conta_codigo_banco = cedente_conta_codigo_banco
        self.cedente_conta_numero = cedente_conta_numero
        self.cedente_conta_numero_dv = cedente_conta_numero_dv
        self.cedente_convenio_numero = cedente_convenio_numero
        self.titulo_aceite = titulo_aceite
        self.titulo_doc_especie = titulo_doc_especie
        self.titulo_local_pagamento = titulo_local_pagamento
        self.titulo_cod_desconto = titulo_cod_desconto
        self.titulo_prazo_desconto = titulo_prazo_desconto
        self.titulo_valor_desconto_taxa = titulo_valor_desconto_taxa
        self.titulo_cod_desconto2 = titulo_cod_desconto2
        self.titulo_prazo_desconto2 = titulo_prazo_desconto2
        self.titulo_valor_desconto_taxa2 = titulo_valor_desconto_taxa2
        self.titulo_codigo_juros = titulo_codigo_juros
        self.titulo_prazo_juros = titulo_prazo_juros
        self.titulo_valor_juros = titulo_valor_juros
        self.titulo_codigo_multa = titulo_codigo_multa
        self.titulo_prazo_multa = titulo_prazo_multa
        self.titulo_valor_multa_taxa = titulo_valor_multa_taxa
        self.titulo_cod_protesto = titulo_cod_protesto
        self.titulo_prazo_protesto = titulo_prazo_protesto
        self.titulo_cod_baixa_devolucao = titulo_cod_baixa_devolucao
        self.titulo_prazo_baixa = titulo_prazo_baixa
        self.titulo_mensagem01 = titulo_mensagem01
        self.titulo_mensagem02 = titulo_mensagem02
        self.titulo_mensagem03 = titulo_mensagem03
        self.titulo_sacador_avalista = titulo_sacador_avalista
        self.titulo_sacador_avalista_endereco = titulo_sacador_avalista_endereco
        self.titulo_sacador_avalista_cidade = titulo_sacador_avalista_cidade
        self.titulo_sacador_avalista_cep = titulo_sacador_avalista_cep
        self.titulo_sacador_avalista_uf = titulo_sacador_avalista_uf
        self.titulo_inscricao_sacador_avalista = titulo_inscricao_sacador_avalista
        self.titulo_emissao_boleto = titulo_emissao_boleto
        self.titulo_categoria = titulo_categoria
        self.titulo_postagem_boleto = titulo_postagem_boleto
        self.titulo_cod_emissao_bloqueto = titulo_cod_emissao_bloqueto
        self.titulo_outros_acrescimos = titulo_outros_acrescimos
        self.titulo_informacoes_adicionais = titulo_informacoes_adicionais
        self.titulo_instrucoes = titulo_instrucoes
        self.titulo_variacao_carteira = titulo_variacao_carteira
        self.deletado = deletado
        if _id:
            self._id = _id

class Cobranca(Base):
    COLLECTION_NAME = 'cobrancas'

    def __init__(self, conta_id, template_boleto_id, sacado_cpf_cnpj, sacado_email, sacado_endereco_logradouro,
            sacado_endereco_numero, sacado_endereco_complemento, sacado_endereco_bairro, sacado_endereco_cep, sacado_endereco_cidade,
            sacado_endereco_uf, sacado_endereco_pais, sacado_nome, sacado_telefone, sacado_celular, titulo_valor,
            titulo_numero_documento, titulo_data_vencimento, created_at=None, _id=None):
        self.conta_id = conta_id
        self.template_boleto_id = template_boleto_id
        self.sacado_cpf_cnpj = sacado_cpf_cnpj
        self.sacado_email = sacado_email
        self.sacado_endereco_logradouro = sacado_endereco_logradouro
        self.sacado_endereco_numero = sacado_endereco_numero
        self.sacado_endereco_complemento = sacado_endereco_complemento
        self.sacado_endereco_bairro = sacado_endereco_bairro
        self.sacado_endereco_cep = sacado_endereco_cep
        self.sacado_endereco_cidade = sacado_endereco_cidade
        self.sacado_endereco_uf = sacado_endereco_uf
        self.sacado_endereco_pais = sacado_endereco_pais
        self.sacado_nome = sacado_nome
        self.sacado_telefone = sacado_telefone
        self.sacado_celular = sacado_celular
        self.titulo_valor = titulo_valor
        self.titulo_numero_documento = titulo_numero_documento
        self.titulo_data_vencimento = titulo_data_vencimento
        self.created_at = created_at if created_at else datetime.datetime.now()
        if _id:
            self._id = _id

    