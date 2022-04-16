from django import forms
from django.db.models import Q

from .models import Conta, Empresa, Endereco, Telefone

class BaseFormWithFormControlBootstrap(forms.ModelForm):
    '''
        Classe base com construtor que altera todos os widgets do tipo text
        para terem a classe form-control do bootstrap
    '''
    def __init__(self, *args, **kwargs):
        super(BaseFormWithFormControlBootstrap, self).__init__(*args, **kwargs)
        for f in self.fields:
            if not type(self.fields[f].widget) in [forms.CheckboxInput, forms.RadioSelect]:
                if 'class' in self.fields[f].widget.attrs:
                    self.fields[f].widget.attrs['class'] += ' form-control'
                else:
                    self.fields[f].widget.attrs['class'] = 'form-control'
        
    

class CriarSenhaContaForm(forms.Form):

    senha1 = forms.CharField(
        label='Informe uma senha',
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    senha2 = forms.CharField(
        label='Confirme a senha',
        max_length=20,
        min_length=6,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        senha1 = cleaned_data.get('senha1')
        senha2 = cleaned_data.get('senha2')

        if senha1 != senha2:
            raise forms.ValidationError('As senhas devem ser iguais.')

class ContasForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContasForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if type(self.fields[f].widget) != forms.RadioSelect:
                if 'class' in self.fields[f].widget.attrs:
                    self.fields[f].widget.attrs['class'] += ' form-control'
                else:
                    self.fields[f].widget.attrs['class'] = 'form-control'
        self.fields['regime_tributario'].choices = self.fields['regime_tributario'].choices[1:]

        tipo_pessoa = self.data['tipo_pessoa'] if len(self.data) > 0 else self.instance.tipo_pessoa
        if tipo_pessoa == Conta.PESSOA_FISICA:
            self.fields['razao_social'].widget.attrs['disabled'] = True
            self.fields['im'].widget.attrs['disabled'] = True
            self.fields['cnae'].widget.attrs['disabled'] = True
            self.fields['regime_tributario'].widget.attrs['disabled'] = True

    class Meta:
        model = Conta
        fields = '__all__'
        exclude = [
            'bitrix_user_id'
        ]

        widgets = {
            'tipo_pessoa': forms.RadioSelect(
                attrs={
                    'class': 'form-check-input',
                }
            ),
            'regime_tributario': forms.RadioSelect(
                attrs={
                    'class': 'form-check-input pj',
                }
            ),
            'cpf_cnpj': forms.TextInput(
                attrs={
                    'class': 'cpf_cnpj',
                }
            ),
            'razao_social': forms.TextInput(
                attrs={
                    'class': 'pj',
                    
                }
            ),
            'im': forms.TextInput(
                attrs={
                    'class': 'pj',
                }
            ),
            'cnae': forms.TextInput(
                attrs={
                    'class': 'pj',
                }
            ),
            'endereco_cep': forms.TextInput(
                attrs={
                    'class': 'cep',
                }
            ),
            'endereco_uf': forms.TextInput(
                attrs={
                    'style': 'text-transform: uppercase',
                }
            ),
            'contato_telefone': forms.TextInput(
                attrs={
                    'class': 'telefone',
                }
            )
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_pessoa = cleaned_data.get('tipo_pessoa')
        regime_tributario = cleaned_data.get('regime_tributario')
        razao_social = cleaned_data.get('razao_social')
        im = cleaned_data.get('im')
        cnae = cleaned_data.get('cnae')

        if tipo_pessoa == Conta.PESSOA_JURIDICA:
            if not regime_tributario:
                self.add_error('regime_tributario', 'Informe um regime tributário')

            if not razao_social:
                self.add_error('razao_social', 'Campo obrigatório.')

            if not im:
                self.add_error('im', 'Campo obrigatório.')

            if not cnae:
                self.add_error('cnae', 'Campo obrigatório.')
        
        return cleaned_data

    def clean_cpf_cnpj(self):
        cpf_cnpj = self.cleaned_data.get('cpf_cnpj')
        if Conta.objects.filter(~Q(id=self.instance.id), cpf_cnpj=cpf_cnpj, is_deletado=False).exists():
            raise forms.ValidationError('Já existe uma Conta com esse CPF/CNPJ')
        return cpf_cnpj

    def clean_contato_email(self):
        contato_email = self.cleaned_data.get('contato_email')
        if Conta.objects.filter(~Q(id=self.instance.id), contato_email=contato_email, is_deletado=False).exists():
            raise forms.ValidationError('Já existe uma Conta com esse e-mail')
        return contato_email

class EmpresaForm(BaseFormWithFormControlBootstrap):

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = [
            'data_cadastro',
            'data_ult_atualizacao',
            'deletado',
            'conta',
        ]

        widgets = {
            'cpf_cnpj': forms.TextInput(
                attrs={
                    'class': 'cnpj',
                }
            ),
            'nome_fantasia': forms.TextInput(),
            'razao_social': forms.TextInput(),
        }

class EnderecoForm(BaseFormWithFormControlBootstrap):

    class Meta:
        model = Endereco
        fields = '__all__'
        exclude = [
            'empresa',
        ]

        widgets = {
            'cep': forms.TextInput(
                attrs={
                    'class': 'cep',
                }
            )
        }

class TelefoneForm(forms.ModelForm):
    class Meta:
        model = Telefone
        fields = [
            'ddd',
            'numero',
        ]

        widgets = {
            'ddd': forms.TextInput(
                attrs={
                    'class': 'form-control col-4',
                    'placeholder': 'DDD',
                }
            ),
            'numero': forms.TextInput(
                attrs={
                    'class': 'telefone form-control',
                    'size': '70',
                    'placeholder': 'Número',
                }
            )
        }

class ServicoForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ServicoForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            if not type(self.fields[f].widget) in [forms.CheckboxInput, forms.RadioSelect]:
                if 'class' in self.fields[f].widget.attrs:
                    self.fields[f].widget.attrs['class'] += ' form-control'
                else:
                    self.fields[f].widget.attrs['class'] = 'form-control'
    
    TOMADOR = 1
    INTERMEDIARIO = 2
    
    RESPONSAVEIS_RETENCAO = (
        (TOMADOR, 'Tomador'),
        (INTERMEDIARIO, 'Intermediário'),
    )

    ISENTO_ISS = 1
    IMUNE = 2
    NAO_INCIDENCIA_MUNICIPIO = 3
    NAO_TRIBUTAVEL = 4
    RETIDO = 5
    TRIBUTAVEL_DENTRO_MUNICIPIO = 6
    TRIBUTAVEL_FORA_MUNICIPIO = 7
    TRIBUTAVEL_DENTRO_MUNICIPIO_TOMADOR = 8
    TIPOS_TRIBUTACOES = (
        (ISENTO_ISS, 'Isento de ISS'),
        (IMUNE, 'Imune'),
        (NAO_INCIDENCIA_MUNICIPIO, 'Não Incidência no Município'),
        (NAO_TRIBUTAVEL, 'Não Tributável'),
        (RETIDO, 'Retido'),
        (TRIBUTAVEL_DENTRO_MUNICIPIO, 'Tributável Dentro do Município'),
        (TRIBUTAVEL_FORA_MUNICIPIO, 'Tributável Fora do Município'),
        (TRIBUTAVEL_DENTRO_MUNICIPIO_TOMADOR, 'Tributável Dentro do Município pelo tomador'),
    )

    EXIGIVEL = 1
    NAO_INCIDENCIA = 2
    ISENCAO = 3
    EXPORTACAO = 4
    IMUNIDADE = 5
    SUSPENSO_ACAO_JUDICIAL = 6
    SUSPENSO_ACAO_ADMINISTRATIVA = 7
    EXIGIBILIDADES = (
        (EXIGIVEL, 'Exigível'),
        (NAO_INCIDENCIA, 'Não Incidência'),
        (ISENCAO, 'Isenção'),
        (EXPORTACAO, 'Exportação'),
        (IMUNIDADE, 'Imunidade'),
        (SUSPENSO_ACAO_JUDICIAL, 'Suspenso por Ação Judicial'),
        (SUSPENSO_ACAO_ADMINISTRATIVA, 'Suspenso por Ação Administrativa'),
    )

    SEM_DEDUCOES = 0
    MATERIAIS = 1
    SUBEMPREITADA_MAO_OBRA = 2
    SERVICOS = 3
    PRODUCAO_EXTERNA = 4
    ALIMENTACAO_BEBIDAS = 5
    REEMBOLSO_DESPESAS = 6
    REPASSE_CONSORCIADO = 7
    REPASSE_PLANO_SAUDE = 8
    OUTRAS_DEDUCOES = 99
    TIPOS_DEDUCOES = (
        (SEM_DEDUCOES, 'Sem Deduções'),
        (MATERIAIS, 'Materiais'),
        (SUBEMPREITADA_MAO_OBRA, 'Subempreitada de Mão de Obra'),
        (SERVICOS, 'Serviços'),
        (PRODUCAO_EXTERNA, 'Produção Externa'),
        (ALIMENTACAO_BEBIDAS, 'Alimentação e Bebidas'),
        (REEMBOLSO_DESPESAS, 'Reembolso de Despesas'),
        (REPASSE_CONSORCIADO, 'Repasse Consorciado'),
        (REPASSE_PLANO_SAUDE, 'Repasse Plano de Saúde'),
        (OUTRAS_DEDUCOES, 'Outras Deduções'),
    )

    codigo = forms.CharField(
        label='Código',
        max_length=10,
    )
    id_integracao = forms.CharField(
        label='Código EXTERNO de integração do serviço',
        help_text='Utilizado SOMENTE quando se cadastra previamente um serviço.',
        max_length=20,
        required=False,
    )
    discriminacao = forms.CharField(
        label='Detalhamento do serviço prestado',
        max_length=1024,
    )

    codigo_tributacao = forms.CharField(
        label='Código tributação no Município',
        max_length=10,
        required=False,
    )

    cnae = forms.CharField(
        label='CNAE',
        max_length=512,
        required=False,
    )

    codigo_cidade_incidencia = forms.CharField(
        label='Codigo IBGE da cidade de incidência do ISS',
        max_length=10,
        required=False,
    )

    descricao_cidade_incidencia = forms.CharField(
        label='Nome da cidade de incidência do ISS',
        max_length=100,
        required=False,
    )

    unidade = forms.CharField(
        label='Unidade de serviço prestado',
        max_length=10,
        required=False,
    )

    quantidade = forms.IntegerField(
        label='Quantidade dos serviços prestados',
        required=False,
    )

    tributavel = forms.BooleanField(
        label='Serviço sujeito a triutação',
        required=False,
    )

    responsavel_retencao = forms.ChoiceField(
        label='Responsável Retenção',
        choices=RESPONSAVEIS_RETENCAO,
    )

    tributos_federais_retidos = forms.BooleanField(
        label='Tributos Federais Retidos',
        required=False,
    )

    iss_tipo_tributacao = forms.ChoiceField(
        label='Tipo de Tributação do Serviço',
        choices=TIPOS_TRIBUTACOES,
        initial=TRIBUTAVEL_DENTRO_MUNICIPIO,
    )

    iss_exigibilidade = forms.ChoiceField(
        label='Exigibilidade do ISS',
        choices=EXIGIBILIDADES,
        initial=EXIGIVEL,
    )

    iss_retido = forms.BooleanField(
        label='Reter ISS',
        required=False,
    )

    iss_aliquota = forms.FloatField(
        label='Aliquota do ISS do serviço prestado',
        min_value=0,
    )

    iss_valor = forms.FloatField(
        label='Valor do ISS',
        min_value=0,
        required=False,
    )

    iss_valor_retido = forms.FloatField(
        label='Valor ISS retido',
        min_value=0,
        required=False,
    )

    iss_processo_suspensao = forms.CharField(
        label='Numero do Processo de Suspensão da Exigibilidade',
        max_length=100,
        required=False,
    )

    obra_art = forms.CharField(
        label='Código do ART',
        max_length=20,
        required=False,
    )

    obra_codigo = forms.CharField(
        label='Código da Obra (CO)',
        max_length=10,
        required=False,
    )

    obra_cei = forms.CharField(
        label='Cadastro específico do INSS',
        max_length=10,
        required=False,
    )

    valor_servico = forms.FloatField(
        label='Valor bruto do serviço prestado',
    )

    valor_base_calculo = forms.FloatField(
        label='Valor da base de cálculo dos impostos',
        required=False,
    )

    valor_deducoes = forms.FloatField(
        label='Valor deduções',
        required=False,
    )

    valor_desconto_condicionado = forms.FloatField(
        label='Valor do desconto condicionado',
        required=False,
    )

    valor_desconto_incondicionado = forms.FloatField(
        label='Valor do desconto incondicionado',
        required=False,
    )

    valor_liquido = forms.FloatField(
        label='Valor líquido do serviço',
        required=False,
    )

    valor_unitario = forms.FloatField(
        label='Valor unitário do serviço',
        required=False,
    )

    valor_aproximado_tributos = forms.FloatField(
        label='Valor aproximado dos tributos. Campo utilizado somente para NFS-e de Brasília',
        required=False,
    )

    deducao_tipo = forms.ChoiceField(
        label='Tipo de Dedução',
        choices=TIPOS_DEDUCOES,
        required=False,
    )

    deducao_descricao = forms.CharField(
        label='Descrição da Dedução',
        max_length=512,
        required=False,
    )

    retencao_pis_base_calculo = forms.FloatField(
        label='Base de cálculo do PIS Retido',
        required=False,
    )

    retencao_pis_aliquota = forms.FloatField(
        label='Alíquota PIS retido',
        required=False,
    )

    retencao_pis_valor = forms.FloatField(
        label='Valor PIS retido',
        required=False,
    )

    retencao_pis_cst = forms.CharField(
        label='Para NFS-e de Brasília: Controla o CST utilizado para emissão da NF-e, por padrão, para optantes do simples nacional, utilizamos 99, para não optantes, utilizamos 01',
        max_length=10,
        required=False,
    )

    retencao_cofins_base_calculo = forms.FloatField(
        label='Base de cálculo do COFINS Retido',
        required=False,
    )

    retencao_cofins_aliquota = forms.FloatField(
        label='Alíquota COFINS retido',
        required=False,
    )

    retencao_cofins_valor = forms.FloatField(
        label='Valor COFINS retido',
        required=False,
    )

    retencao_cofins_cst = forms.CharField(
        label='Para NFS-e de Brasília: Controla o CST utilizado para emissão da NF-e, por padrão, para optantes do simples nacional, utilizamos 99, para não optantes, utilizamos 01',
        max_length=10,
        required=False,
    )

    retencao_csll_aliquota = forms.FloatField(
        label='Alíquota CSLL retido',
        required=False,
    )

    retencao_csll_valor = forms.FloatField(
        label='Valor CSLL retido',
        required=False,
    )

    retencao_inss_aliquota = forms.FloatField(
        label='Alíquota INSS retido',
        required=False,
    )

    retencao_inss_valor = forms.FloatField(
        label='Valor INSS retido',
        required=False,
    )

    retencao_irrf_aliquota = forms.FloatField(
        label='Alíquota IRRF retido',
        required=False,
    )

    retencao_irrf_valor = forms.FloatField(
        label='Valor IRRF retido',
        required=False,
    )

    retencao_cpp_aliquota = forms.FloatField(
        label='Alíquota CPP retido',
        required=False,
    )

    retencao_cpp_valor = forms.FloatField(
        label='Valor CPP retido',
        required=False,
    )

    retencao_outras_retencoes = forms.FloatField(
        label='Valor de outras retenções',
        required=False,
    )

    ibpt_simplificado_aliquota = forms.FloatField(
        label='Aliquota Geral de Impostos',
        required=False,
    )

    ibpt_detalhado_aliquota_municipal = forms.FloatField(
        label='Aliquota municipal de impostos',
        required=False,
    )

    ibpt_detalhado_aliquota_estadual = forms.FloatField(
        label='Aliquota estadual de impostos',
        required=False,
    )

    ibpt_detalhado_aliquota_federal = forms.FloatField(
        label='Aliquota federal de impostos',
        required=False,
    )