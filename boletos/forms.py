from django import forms

ACEITO = 'S'
NAO_ACEITO = 'N'
TITULO_ACEITE = (
    (ACEITO, f'{ACEITO} - Aceito'),
    (NAO_ACEITO, f'{NAO_ACEITO} - Não aceito'),
)

SEM_INSTRUCAO_DESCONTO = 0
VALOR_FIXO_ATE_DATA_INFORMADA = 1
PERCENTUAL_ATE_DATA_INFORMADA = 2
VALOR_ANTECIPACAO_DIA_CORRIDO = 3
VALOR_ANTECIPACAO_DIA_UTIL = 4
PERCENTUAL_SOBRE_VALOR_NOMINAL_DIA_CORRIDO = 5
PERCENTUAL_SOBRE_VALOR_NOMINAL_DIA_UTIL = 6
CANCELAMENTO_DESCONTO = 7
TITULO_COD_DESCONTO = (
    (SEM_INSTRUCAO_DESCONTO, f'{SEM_INSTRUCAO_DESCONTO} - Sem instrução de desconto'),
    (VALOR_FIXO_ATE_DATA_INFORMADA, f'{VALOR_FIXO_ATE_DATA_INFORMADA} - Valor Fixo Até a Data Informada'),
    (PERCENTUAL_ATE_DATA_INFORMADA, f'{PERCENTUAL_ATE_DATA_INFORMADA} - Percentual Até a Data Informada'),
    (VALOR_ANTECIPACAO_DIA_CORRIDO, f'{VALOR_ANTECIPACAO_DIA_CORRIDO} - Valor por Antecipação Dia Corrido'),
    (VALOR_ANTECIPACAO_DIA_UTIL, f'{VALOR_ANTECIPACAO_DIA_UTIL} - Valor por Antecipação Dia Útil'),
    (PERCENTUAL_SOBRE_VALOR_NOMINAL_DIA_CORRIDO, f'{PERCENTUAL_SOBRE_VALOR_NOMINAL_DIA_CORRIDO} - Percentual Sobre o Valor Nominal Dia Corrido'),
    (PERCENTUAL_SOBRE_VALOR_NOMINAL_DIA_UTIL, f'{PERCENTUAL_SOBRE_VALOR_NOMINAL_DIA_UTIL} - Percentual Sobre o Valor Nominal Dia Útil'),
    (CANCELAMENTO_DESCONTO, f'{CANCELAMENTO_DESCONTO} - Cancelamento de Desconto'),
)

VALOR_POR_DIA = 1
TAXA_MENSAL = 2
TITULO_CODIGO_JUROS = (
    (VALOR_POR_DIA, f'{VALOR_POR_DIA} - Valor por dia'),
    (TAXA_MENSAL, f'{TAXA_MENSAL} - Taxa mensal'),
)

NAO_REGISTRA_MULTA = 0
VALOR_EM_REAIS = 1
VALOR_EM_PERCENTUAL = 2
TITULO_CODIGO_MULTA = (
    (NAO_REGISTRA_MULTA, f'{NAO_REGISTRA_MULTA} - Não registra a multa'),
    (VALOR_EM_REAIS, f'{VALOR_EM_REAIS} - Valor em Reais (Fixo)'),
    (VALOR_EM_PERCENTUAL, f'{VALOR_EM_PERCENTUAL} - Valor em percentual com duas casas decimais'),
)

PROTESTAR_DIAS_CORRIDOS = 1
PROTESTAR_DIAS_UTEIS = 2
NAO_PROTESTAR = 3
PROTESTAR_FIM_FALIMENTAR_DIAS_UTEIS = 4
PROTESTAR_FIM_FALIMENTAR_DIAS_CORRIDOS = 5
NEGATIVACAO_SEM_PROTESTO = 8
CANCELAMENTO_PROTESTO_AUTOMATICO = 9 # SOMENTE VÁLIDO PARA CODIGO MOVIMENTO REMESSA = 31
TITULO_CODIGO_PROTESTO = (
    (PROTESTAR_DIAS_CORRIDOS, f'{PROTESTAR_DIAS_CORRIDOS} - Protestar Dias Corridos'),
    (PROTESTAR_DIAS_UTEIS, f'{PROTESTAR_DIAS_UTEIS} - Protestar Dias Úteis'),
    (NAO_PROTESTAR, f'{NAO_PROTESTAR} - Não Protestar'),
    (PROTESTAR_FIM_FALIMENTAR_DIAS_UTEIS, f'{PROTESTAR_FIM_FALIMENTAR_DIAS_UTEIS} - Protestar Fim Falimentar - Dias Úteis'),
    (PROTESTAR_FIM_FALIMENTAR_DIAS_CORRIDOS, f'{PROTESTAR_FIM_FALIMENTAR_DIAS_CORRIDOS} - Protestar Fim Falimentar - Dias Corridos'),
    (NEGATIVACAO_SEM_PROTESTO, f'{NEGATIVACAO_SEM_PROTESTO} - Negativação sem Protesto'),
    (CANCELAMENTO_PROTESTO_AUTOMATICO, f'{CANCELAMENTO_PROTESTO_AUTOMATICO} - Cancelamento Protesto Automático'),
)

BAIXAR_DEVOLVER = 1
NAO_BAIXAR_NAO_DEVOLVER = 2
CANCELAR_PRAZO_BAIXA_DEVOLUCAO = 3
TITULO_CODIGO_BAIXA_DEVOLUCAO = (
    (BAIXAR_DEVOLVER, f'{BAIXAR_DEVOLVER} - Baixar/Devolver'),
    (NAO_BAIXAR_NAO_DEVOLVER, f'{NAO_BAIXAR_NAO_DEVOLVER} - Não Baixar / Não Devolver'),
    (CANCELAR_PRAZO_BAIXA_DEVOLUCAO, f'{CANCELAR_PRAZO_BAIXA_DEVOLUCAO} - Cancelar prazo para baixa / Devolução'),
)

IMPRESSAO_REALIZADO_PELO_BANCO = 'A'
IMPRESSAO_REALIZADO_PELO_BENEFICIARIO = 'B'
TITULO_EMISSAO_BOLETO = (
    (IMPRESSAO_REALIZADO_PELO_BANCO, f'{IMPRESSAO_REALIZADO_PELO_BANCO} - Impressão será realizado pelo banco'),
    (IMPRESSAO_REALIZADO_PELO_BENEFICIARIO, f'{IMPRESSAO_REALIZADO_PELO_BENEFICIARIO} - Impressão será realizado pelo beneficiário'),
)

SEM_REGISTRO = 1
COM_REGISTRO = 2
IMPRESSAO_PELO_BANCO = 3
TITULO_CATEGORIA = (
    (SEM_REGISTRO, f'{SEM_REGISTRO} - Sem registro'),
    (COM_REGISTRO, f'{COM_REGISTRO} - Com registro'),
    (IMPRESSAO_PELO_BANCO, f'{IMPRESSAO_PELO_BANCO} - Impressão pelo banco'),
)

POSTAGEM_PELO_BANCO = 'S'
POSTAGEM_RESPONSABILIDADE_CEDENTE = 'N'
TITULO_POSTAGEM_BOLETO = (
    (POSTAGEM_PELO_BANCO, f'{POSTAGEM_PELO_BANCO} - Postagem pelo banco'),
    (POSTAGEM_RESPONSABILIDADE_CEDENTE, f'{POSTAGEM_RESPONSABILIDADE_CEDENTE} - Postagem por responsabilidade do cedente'),
)

BANCO_EMITE = 1
CLIENTE_EMITE = 2
BANCO_PRE_EMITE_CLIENTE_COMPLEMENTA = 3
BANCO_REEMITE = 4
BANCO_NAO_REEMITE = 5
BANCO_EMITENTE_ABERTA = 7
BANCO_EMITENTE_AUTO_ENVELOPAVEL = 8
TITULO_CODIGO_EMISSAO_BLOQUETO = (
    (BANCO_EMITE, f'{BANCO_EMITE} - Banco Emite'),
    (CLIENTE_EMITE, f'{CLIENTE_EMITE} - Cliente Emite'),
    (BANCO_PRE_EMITE_CLIENTE_COMPLEMENTA, f'{BANCO_PRE_EMITE_CLIENTE_COMPLEMENTA} - Banco Pré-emite e Cliente Complementa'),
    (BANCO_REEMITE, f'{BANCO_REEMITE} - Banco Reemite'),
    (BANCO_NAO_REEMITE, f'{BANCO_NAO_REEMITE} - Banco Não Reemite'),
    (BANCO_EMITENTE_ABERTA, f'{BANCO_EMITENTE_ABERTA} - Banco Emitente - Aberta'),
    (BANCO_EMITENTE_AUTO_ENVELOPAVEL, f'{BANCO_EMITENTE_AUTO_ENVELOPAVEL} - Banco Emitente - Auto-envelopável'),
)

class TemplateBoletoForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(TemplateBoletoForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].widget.attrs['class'] = 'form-control'
            if type(self.fields[f]) == forms.DateField:
                self.fields[f].widget.attrs['class'] += ' data'
    
    
    descricao = forms.CharField(
        label='Descrição',
        max_length=100,
    )

    cedente_conta_codigo_banco = forms.CharField(
        label='Conta Código Banco',
        max_length=10,
    )

    cedente_conta_numero = forms.CharField(
        label='Conta Número',
        max_length=20,
    )

    cedente_conta_numero_dv = forms.CharField(
        label='Conta Número DV',
        max_length=10
    )
    cedente_convenio_numero = forms.CharField(
        label='Convênio Número',
        max_length=20,
    )
    
    titulo_aceite = forms.ChoiceField(
        label='Aceite',
        choices=TITULO_ACEITE,
    )
    
    titulo_doc_especie = forms.CharField(
        label='Doc Espécie',
        max_length=5,
    )
    
    titulo_local_pagamento = forms.CharField(
        label='Local Pagamento',
        max_length=200,
        initial='Pagavel em qualquer banco até o vencimento'
    )

    titulo_cod_desconto = forms.ChoiceField(
        label='Código Desconto 1',
        choices=TITULO_COD_DESCONTO,
    )

    titulo_prazo_desconto = forms.DateField(
        label='Data Desconto 1',
    )
    titulo_valor_desconto_taxa = forms.FloatField(
        label='Valor Desconto Taxa 1',
        initial=0.00,
    )
    titulo_cod_desconto2 = forms.ChoiceField(
        label='Código Desconto 2',
        choices=TITULO_COD_DESCONTO,
    )
    titulo_prazo_desconto2 = forms.DateField(
        label='Data Desconto 2',
    )
    titulo_valor_desconto_taxa2 = forms.FloatField(
        label='Valor Desconto Taxa 2',
        initial=0.00,
    )
    titulo_codigo_juros = forms.ChoiceField(
        label='Código Juros',
        choices=TITULO_CODIGO_JUROS,
    )
    titulo_prazo_juros = forms.DateField(
        label='Prazo Juros',
    )

    titulo_valor_juros = forms.FloatField(
        label='Valor Juros',
    )
    titulo_codigo_multa = forms.ChoiceField(
        label='Título Codigo Multa',
        choices=TITULO_CODIGO_MULTA
    )
    titulo_prazo_multa = forms.DateField(
        label='Título Prazo Multa',
    )
    titulo_valor_multa_taxa = forms.FloatField(
        label='Titulo Valor Multa Taxa',
    )
    titulo_cod_protesto = forms.ChoiceField(
        label='Título Código Protesto',
        choices=TITULO_CODIGO_PROTESTO,
    )
    titulo_prazo_protesto = forms.IntegerField(
        label='Título Prazo Protesto',
        min_value=0,
        max_value=30,
    )
    titulo_cod_baixa_devolucao = forms.ChoiceField(
        label='Título Código Baixa / Devolução',
        choices=TITULO_CODIGO_BAIXA_DEVOLUCAO,
    )
    titulo_prazo_baixa = forms.IntegerField(
        label='Título Prazo Baixa',
        min_value=0,
        max_value=30,
    )
    titulo_mensagem01 = forms.CharField(
        label='Título Mensagem 01',
        max_length=80,
    )
    titulo_mensagem02 = forms.CharField(
        label='Título Mensagem 02',
        max_length=80,
    )
    titulo_mensagem03 = forms.CharField(
        label='Título Mensagem 03',
        max_length=80,
    )
    titulo_sacador_avalista = forms.CharField(
        label='Nome',
        max_length=200,
    )
    titulo_sacador_avalista_endereco = forms.CharField(
        label='Endereço',
        max_length=200,
    )
    titulo_sacador_avalista_cidade = forms.CharField(
        label='Cidade',
        max_length=50,
    )
    titulo_sacador_avalista_cep = forms.CharField(
        label='CEP',
        max_length=8,
    )
    titulo_sacador_avalista_uf = forms.CharField(
        label='UF',
        max_length=5,
    )
    titulo_inscricao_sacador_avalista = forms.CharField(
        label='CPF/CNPJ',
        max_length=15,
    )
    titulo_emissao_boleto = forms.ChoiceField( # APENAS PARA O BANCO SICREDI CNAB400
        label='Título Emissão Boleto',
        choices=TITULO_EMISSAO_BOLETO,
    )
    titulo_categoria = forms.ChoiceField(
        label='Título Categoria',
        choices=TITULO_CATEGORIA,
    )
    titulo_postagem_boleto = forms.ChoiceField(
        label='Título Postagem Boleto',
        choices=TITULO_POSTAGEM_BOLETO,
    )
    titulo_cod_emissao_bloqueto = forms.ChoiceField(
        label='Título Código Emissão Bloqueto',
        choices=TITULO_CODIGO_EMISSAO_BLOQUETO
    )
    titulo_outros_acrescimos = forms.FloatField(
        label='Título Outros Acréscimos',
    )
    titulo_informacoes_adicionais = forms.CharField(
        label='Título Informações Adicionais',
        max_length=100
    )
    titulo_instrucoes = forms.CharField(
        label='Título Instruções',
        max_length=100,
    )
    titulo_variacao_carteira = forms.CharField(
        label='Título Variação Carteira',
        max_length=3,
        required=False,
    )