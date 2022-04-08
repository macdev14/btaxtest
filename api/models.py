import uuid
from django.db import models

from core.models import Conta

class Job(models.Model):
    EMISSAO = 1
    CANCELAMENTO = 2
    ENVIAR = 3
    ENVIADO = 4
    AGUARDANDO = 5
    RETORNADO = 6
    DISPONIVEL = 7
    
    OPERACOES = (
        (EMISSAO, 'Emissão'),
        (CANCELAMENTO, 'Cancelamento'),
    )

    STATUS = (
        (ENVIAR, 'Enviar'),
        (ENVIADO, 'Enviado'),
        (AGUARDANDO, 'Aguardando'),
        (RETORNADO, 'Retornado'),
    )

    STATUS_INTEGRACAO_RETORNO = (
        (DISPONIVEL, 'Disponível'),
        (RETORNADO, 'Retornado'),
    )


    id = models.UUIDField(
        'ID',
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    conta = models.ForeignKey(
        Conta,
        related_name='jobs',
        on_delete=models.CASCADE,
    )

    cnpj_emitente = models.CharField(
        'CNPJ do Emitente',
        max_length=20,
    )

    operacao = models.IntegerField(
        'Operação',
        choices=OPERACOES,
    )

    data_entrada = models.DateTimeField(
        'Data de Entrada',
        auto_now_add=True,
    )

    data_resposta = models.DateTimeField(
        'Data de Resposta',
        null=True,
    )

    status = models.IntegerField(
        'Status',
        choices=STATUS,
    )

    status_integracao_retorno = models.IntegerField(
        'Status Integração Retorno',
        choices=STATUS_INTEGRACAO_RETORNO,
        null=False,
    )

    payload_operacao = models.TextField(
        'Payload da Operação',
        max_length=5120,
        null=True,
    )