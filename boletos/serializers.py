from rest_framework import serializers

from bson.objectid import ObjectId

from boletos.models import Cobranca, TemplateBoleto, Boleto
from mongodb import querys
from core.models import Conta

class CobrancaSerializer(serializers.Serializer):
    template_boleto_id = serializers.CharField()
    sacado_cpf_cnpj = serializers.CharField(
        min_length=11,
        max_length=14,
    )
    sacado_email = serializers.EmailField(
        min_length=1,
        max_length=500,
    )
    sacado_endereco_logradouro = serializers.CharField(
        min_length=1,
        max_length=200,
    )
    sacado_endereco_numero = serializers.CharField(
        min_length=1,
        max_length=20,
    )
    sacado_endereco_complemento = serializers.CharField(
        min_length=1,
        max_length=100,
        allow_blank=True,
    )
    sacado_endereco_bairro = serializers.CharField(
        min_length=1,
        max_length=100,
    )
    sacado_endereco_cep = serializers.CharField(
        min_length=1,
        max_length=9,
    )
    sacado_endereco_cidade = serializers.CharField(
        min_length=1,
        max_length=50,
    )
    sacado_endereco_uf = serializers.CharField(
        min_length=1,
        max_length=2,
    )
    sacado_endereco_pais = serializers.CharField(
        min_length=1,
        max_length=50,
    )
    sacado_nome = serializers.CharField(
        min_length=1,
        max_length=200,
    )
    sacado_telefone = serializers.CharField(
        min_length=1,
        max_length=20,
    )
    sacado_celular = serializers.CharField(
        min_length=1,
        max_length=20,
    )
    titulo_valor = serializers.FloatField()
    titulo_numero_documento = serializers.CharField(
        min_length=1,
        max_length=50,
    )
    titulo_data_vencimento = serializers.DateField(format='%d/%m/%Y')
    
    def __init__(self, conta, *args, **kwargs):
        self.conta = conta
        super(CobrancaSerializer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        return Cobranca(conta_id=self.conta.id, **validated_data)

    def update(self, instance, validated_data):
        instance.template_boleto_id = validated_data.get('template_boleto_id', instance.template_boleto_id)
        instance.sacado_cpf_cnpj = validated_data.get('sacado_cpf_cnpj', instance.sacado_cpf_cnpj)
        instance.sacado_email = validated_data.get('sacado_email', instance.sacado_email)
        instance.sacado_endereco_logradouro = validated_data.get('sacado_endereco_logradouro', instance.sacado_endereco_logradouro)
        instance.sacado_endereco_numero = validated_data.get('sacado_endereco_numero', instance.sacado_endereco_numero)
        instance.sacado_endereco_complemento = validated_data.get('sacado_endereco_complemento', instance.sacado_endereco_complemento)
        instance.sacado_endereco_bairro = validated_data.get('sacado_endereco_bairro', instance.sacado_endereco_bairro)
        instance.sacado_endereco_cep = validated_data.get('sacado_endereco_cep', instance.sacado_endereco_cep)
        instance.sacado_endereco_cidade = validated_data.get('sacado_endereco_cidade', instance.sacado_endereco_cidade)
        instance.sacado_endereco_uf = validated_data.get('sacado_endereco_uf', instance.sacado_endereco_uf)
        instance.sacado_endereco_pais = validated_data.get('sacado_endereco_pais', instance.sacado_endereco_pais)
        instance.sacado_nome = validated_data.get('sacado_nome', instance.sacado_nome)
        instance.sacado_telefone = validated_data.get('sacado_telefone', instance.sacado_telefone)
        instance.sacado_celular = validated_data.get('sacado_celular', instance.sacado_celular)
        instance.titulo_valor = validated_data.get('titulo_valor', instance.titulo_valor)
        instance.titulo_numero_documento = validated_data.get('titulo_numero_documento', instance.titulo_numero_documento)
        instance.titulo_data_vencimento = validated_data.get('titulo_data_vencimento', instance.titulo_data_vencimento)

    def validate(self, data):
        template_boleto_id = data.get('template_boleto_id', None)

        if not querys.get_obj_by_id(TemplateBoleto.COLLECTION_NAME, template_boleto_id):
            raise serializers.ValidationError({'template_boleto_id': 'Template de boleto não encontrado.'})

        return data

class BoletoSerializer(serializers.Serializer):
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

    cedente_cpf_cnpj = serializers.CharField()
    cedente_conta_numero = serializers.CharField()
    cedente_conta_numero_dv = serializers.CharField()
    cedente_conta_codigo_banco = serializers.CharField()
    cedente_convenio_numero = serializers.CharField()
    sacado_cpf_cnpj = serializers.CharField()
    sacado_email = serializers.CharField()
    sacado_endereco_numero = serializers.CharField()
    sacado_endereco_bairro = serializers.CharField()
    sacado_endereco_cep = serializers.CharField()
    sacado_endereco_cidade = serializers.CharField()
    sacado_endereco_complemento = serializers.CharField()
    sacado_endereco_logradouro = serializers.CharField()
    sacado_endereco_pais = serializers.CharField()
    sacado_endereco_uf = serializers.CharField()
    sacado_nome = serializers.CharField()
    sacado_telefone = serializers.CharField()
    sacado_celular = serializers.CharField()
    titulo_data_emissao = serializers.DateField(format='%d/%m/%Y')
    titulo_data_vencimento = serializers.DateField(format='%d/%m/%Y')
    titulo_mensagem01 = serializers.CharField()
    titulo_mensagem02 = serializers.CharField()
    titulo_mensagem03 = serializers.CharField()
    titulo_nosso_numero = serializers.CharField()
    titulo_numero_documento = serializers.CharField()
    titulo_valor = serializers.CharField()
    titulo_local_pagamento = serializers.CharField()
    cobranca_id = serializers.CharField(allow_blank=True)
    situacao = serializers.ChoiceField(choices=SITUACOES, allow_blank=False)

    def create(self, validated_data):
        return Boleto(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.cedente_cpf_cnpj = validated_data.get('cedente_cpf_cnpj', instance.cedente_cpf_cnpj)
        instance.cedente_conta_numero = validated_data.get('cedente_conta_numero', instance.cedente_conta_numero)
        instance.cedente_conta_numero_dv = validated_data.get('cedente_conta_numero_dv', instance.cedente_conta_numero_dv)
        instance.cedente_conta_codigo_banco = validated_data.get('cedente_conta_codigo_banco', instance.cedente_conta_codigo_banco)
        instance.cedente_convenio_numero = validated_data.get('cedente_convenio_numero', instance.cedente_convenio_numero)
        instance.sacado_cpf_cnpj = validated_data.get('sacado_cpf_cnpj', instance.sacado_cpf_cnpj)
        instance.sacado_email = validated_data.get('sacado_email', instance.sacado_email)
        instance.sacado_endereco_numero = validated_data.get('sacado_endereco_numero', instance.sacado_endereco_numero)
        instance.sacado_endereco_bairro = validated_data.get('sacado_endereco_bairro', instance.sacado_endereco_bairro)
        instance.sacado_endereco_cep = validated_data.get('sacado_endereco_cep', instance.sacado_endereco_cep)
        instance.sacado_endereco_cidade = validated_data.get('sacado_endereco_cidade', instance.sacado_endereco_cidade)
        instance.sacado_endereco_complemento = validated_data.get('sacado_endereco_complemento', instance.sacado_endereco_complemento)
        instance.sacado_endereco_logradouro = validated_data.get('sacado_endereco_logradouro', instance.sacado_endereco_logradouro)
        instance.sacado_endereco_pais = validated_data.get('sacado_endereco_pais', instance.sacado_endereco_pais)
        instance.sacado_endereco_uf = validated_data.get('sacado_endereco_uf', instance.sacado_endereco_uf)
        instance.sacado_nome = validated_data.get('sacado_nome', instance.sacado_nome)
        instance.sacado_telefone = validated_data.get('sacado_telefone', instance.sacado_telefone)
        instance.sacado_celular = validated_data.get('sacado_celular', instance.sacado_celular)
        instance.titulo_data_emissao = validated_data.get('titulo_data_emissao', instance.titulo_data_emissao)
        instance.titulo_data_vencimento = validated_data.get('titulo_data_vencimento', instance.titulo_data_vencimento)
        instance.titulo_mensagem01 = validated_data.get('titulo_mensagem01', instance.titulo_mensagem01)
        instance.titulo_mensagem02 = validated_data.get('titulo_mensagem02', instance.titulo_mensagem02)
        instance.titulo_mensagem03 = validated_data.get('titulo_mensagem03', instance.titulo_mensagem03)
        instance.titulo_nosso_numero = validated_data.get('titulo_nosso_numero', instance.titulo_nosso_numero)
        instance.titulo_numero_documento = validated_data.get('titulo_numero_documento', instance.titulo_numero_documento)
        instance.titulo_valor = validated_data.get('titulo_valor', instance.titulo_valor)
        instance.titulo_local_pagamento = validated_data.get('titulo_local_pagamento', instance.titulo_local_pagamento)
        instance.cobranca_id = validated_data.get('cobranca_id', instance.cobranca_id)
        instance.situacao = validated_data.get('situacao', instance.situacao)

        querys.update_obj(self.COLLECTION_NAME, {'_id': ObjectId(instance.id)}, **{instance.data})
