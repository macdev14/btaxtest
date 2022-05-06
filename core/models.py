import uuid, os
from django.db import models

from autenticacao.models import User

def profile_foto_upload(self, filename):
    name, ext = os.path.splitext(filename)

    return f'profiles/foto/{uuid.uuid4}{ext}'

class EstadoEnum(models.TextChoices):
    '''
        Classe Enum usada para setar o choices de campos de Estado
    '''
    AC = 'AC', 'AC'
    AL = 'AL', 'AL'
    AM = 'AM', 'AM'
    AP = 'AP', 'AP'
    BA = 'BA', 'BA'
    CE = 'CE', 'CE'
    DF = 'DF', 'DF'
    ES = 'ES', 'ES'
    GO = 'GO', 'GO'
    MA = 'MA', 'MA'
    MG = 'MG', 'MG'
    MS = 'MS', 'MS'
    MT = 'MT', 'MT'
    PA = 'PA', 'PA'
    PB = 'PB', 'PB'
    PE = 'PE', 'PE'
    PI = 'PI', 'PI'
    PR = 'PR', 'PR'
    RJ = 'RJ', 'RJ'
    RN = 'RN', 'RN'
    RO = 'RO', 'RO'
    RR = 'RR', 'RR'
    RS = 'RS', 'RS'
    SC = 'SC', 'SC'
    SE = 'SE', 'SE'
    SP = 'SP', 'SP'
    TO = 'TO', 'TO'

class TipoLogradouroEnum(models.TextChoices):
    ALAMEDA = 'alameda', 'Alameda'
    AVENIDA = 'avenida', 'Avenida'
    CHACARA = 'chacara', 'Chácara'
    COLONIA = 'colonia', 'Colônia'
    CONDOMINIO = 'condominio', 'Condomínio'
    ESTANCIA = 'estancia', 'Estância'
    ESTRADA = 'estrada', 'Estrada'
    FAZENDA = 'fazenda', 'Fazenda'
    PRACA = 'praca', 'Praça'
    PROLONGAMENTO = 'prolongamento', 'Prolongamento'
    RODOVIA = 'rodovia', 'Rodovia'
    RUA = 'rua', 'Rua'
    SITIO = 'sitio', 'Sítio'
    TRAVESSA = 'travessa', 'travessa'
    VICINAL = 'vicinal', 'Vicinal'

class TipoBairroEnum(models.TextChoices):

    BAIRRO = 'bairro', 'Bairro'
    BOSQUE = 'bosque', 'Bosque'
    CHACARA = 'chacara', 'Chácara'
    CONJUNTO = 'conjunto', 'Conjunto'
    DESMEMBRAMENTO = 'desmembramento', 'Desmembramento'
    DISTRITO = 'distrito', 'Distrito'
    FAVELA = 'favela', 'Favela'
    FAZENDA = 'fazenda', 'Fazenda'
    GLEBA = 'gleba', 'Gleba'
    HORTO = 'horto', 'Horto'
    JARDIM = 'jardim', 'Jardim'
    LOTEAMENTO = 'loteamento', 'Loteamento'
    NUCLEO = 'nucleo', 'Núcleo'
    PARQUE = 'parque', 'Parque'
    RESIDENCIAL = 'residencial', 'Residencial'
    SITIO = 'sitio', 'Sítio'
    TROPICAL = 'tropical', 'Tropical'
    VILA = 'vila', 'Vila'
    ZONA = 'zona', 'Zona'
    CENTRO = 'centro', 'Centro'
    SETOR = 'setor', 'Setor'
    
class Conta(models.Model):

    PESSOA_FISICA = 'F'
    PESSOA_JURIDICA = 'J'
    TIPO_PESSOA = (
        (PESSOA_FISICA, 'Pessoa Física'),
        (PESSOA_JURIDICA, 'Pessoa Jurídica'),
    )

    SIMPLES_NACIONAL = 'SN'
    REGIME_APURACAO = 'RA'
    REGIME_TRIBUTARIO = (
        (SIMPLES_NACIONAL, 'Simples Nacional'),
        (REGIME_APURACAO, 'Regime de Apuração'),
    )

    id = models.UUIDField(
        'Id',
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    nome = models.CharField(
        'Nome',
        max_length=30,
    )

    razao_social = models.CharField(
        'Razão Social',
        max_length=50,
        null=True,
        blank=True,
    )

    tipo_pessoa = models.CharField(
        'Tipo de Pessoa',
        choices=TIPO_PESSOA,
        max_length=1,
        default=PESSOA_FISICA,
    )

    cpf_cnpj = models.CharField(
        'CPF/CNPJ',
        max_length=20,
    )

    rg_ie = models.CharField(
        'RG/I.E.',
        max_length=17,
        null=True,
        blank=True,
    )

    im = models.CharField(
        'IM',
        max_length=12,
        null=True,
        blank=True,
    )

    cnae = models.CharField(
        'CNAE',
        max_length=7,
        null=True,
        blank=True,
    )

    regime_tributario = models.CharField(
        'Regime Tributário',
        max_length=2,
        choices=REGIME_TRIBUTARIO,
        null=True,
        blank=True,
    )

    endereco_cep = models.CharField(
        'CEP',
        max_length=9,
    )

    endereco_cidade = models.CharField(
        'Cidade',
        max_length=100,
    )

    endereco_uf = models.CharField(
        'UF',
        max_length=2,
        choices=EstadoEnum.choices,
    )

    endereco_logradouro = models.CharField(
        'Endereço',
        max_length=150,
    )

    endereco_numero = models.CharField(
        'Número',
        max_length=10,
    )

    endereco_complemento = models.CharField(
        'Complemento',
        max_length=50,
        null=True,
        blank=True,
    )

    endereco_bairro = models.CharField(
        'Bairro',
        max_length=100,
    )

    contato_nome = models.CharField(
        'Nome Contato',
        max_length=100,
        null=True,
    )

    contato_telefone = models.CharField(
        'Telefone',
        max_length=20,
    )

    contato_email = models.EmailField(
        'E-mail',
        max_length=150,
    )

    bitrix_user_id = models.CharField(
        'ID Usuário Bitrix',
        max_length=50,
        null=True,
    )

    id_cedente = models.CharField(
        'ID Usuário TechnoSpeed',
        max_length=50,
        null=True,
        blank=True
    )

    is_deletado = models.BooleanField(
        'Deletado?',
        default=False,
    )

    def delete(self):
        self.is_deletado = True
        self.save()

    def __str__(self):
        return self.nome


class Profile(models.Model):

    id = models.UUIDField(
        'Id',
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    conta = models.ForeignKey(
        'Conta',
        related_name='profiles',
        on_delete=models.CASCADE,
    )

    usuario = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE
    )

    data_criacao = models.DateTimeField(
        'Data da Criação',
        auto_now_add=True,
    )

    data_atualizacao = models.DateTimeField(
        'Data da Última Atualizacao',
        auto_now=True,
    )

    foto = models.ImageField(
        'Foto',
        upload_to=profile_foto_upload,
        null=True,
        blank=True,
    )

    nome = models.CharField(
        'Nome',
        max_length=150,
        null=True,
    )

    email = models.EmailField(
        'E-mail',
        max_length=150,
    )

    telefone = models.CharField(
        'Telefone',
        max_length=18,
        null=True,
        blank=True,
    )

    is_redefinicao_senha = models.BooleanField(
        'Redefinição de senha?',
        default=True,
    )

    is_deletado = models.BooleanField(
        'Deletado?',
        default=False,
    )

    is_principal = models.BooleanField(
        'É o usuário principal da conta?',
        default=False,
    )

    def delete(self):
        self.is_deletado = True
        self.save()

    def __str__(self):
        return self.nome

class Empresa(models.Model):

    NENHUM = 0
    SIMPLES_NACIONAL = 1
    SIMPLES_NACIONAL_EXCESSO = 2
    NORMAL_LUCRO_PRESUMIDO = 3
    NORMAL_LUCRO_REAL = 4
    REGIME_TRIBUTARIO = (
        (NENHUM, 'Nenhum'),
        (SIMPLES_NACIONAL, 'Simples Nacional'),
        (SIMPLES_NACIONAL_EXCESSO, 'Simples Nacional - Excesso'),
        (NORMAL_LUCRO_PRESUMIDO, 'Normal - Lucro Presumido'),
        (NORMAL_LUCRO_REAL, 'Normal - Lucro Real'),
    )

    SEM_REGIME_TRIBUTARIO_ESPECIAL = 0
    MICRO_EMPRESA_MUNICIPAL = 1
    ESTIMATIVA = 2
    SOCIEDADE_PROFISSIONAIS = 3
    COOPERATIVA = 4
    MICROEMPRESARIO_INDIVIDUAL = 5
    MICROEMPRESA_PESQUENO_PORTE = 6
    REGIME_TRIBUTARIO_ESPECIAL = (
        (SEM_REGIME_TRIBUTARIO_ESPECIAL, 'Sem Regime Tributário Especial'),
        (MICRO_EMPRESA_MUNICIPAL, 'Micro Empresa Municipal'),
        (ESTIMATIVA, 'Estimativa'),
        (SOCIEDADE_PROFISSIONAIS, 'Sociedade de Profissionais'),
        (COOPERATIVA, 'Cooperativa'),
        (MICROEMPRESARIO_INDIVIDUAL, 'Microempresário Individual - MEI'),
        (MICROEMPRESA_PESQUENO_PORTE, 'Microempresa ou Pesqueno Porte - ME EPP'),
    )

    conta = models.ForeignKey(
        'Conta',
        related_name='empresas',
        on_delete=models.CASCADE,
    )

    id = models.UUIDField(
        'Id',
        primary_key=True,
        editable=False,
        default=uuid.uuid4,
    )

    data_cadastro = models.DateTimeField(
        'Data de Cadastro',
        auto_now_add=True,
    )

    data_ult_atualizacao = models.DateTimeField(
        'Data da Última Atualização',
        auto_now=True,
    )

    cpf_cnpj = models.CharField(
        'CNPJ',
        max_length=20,
        unique=True,
    )

    inscricao_municipal = models.CharField(
        'Inscrição Municipal',
        max_length=30,
        null=True,
        blank=True,
    )

    inscricao_estadual = models.CharField(
        'Inscrição Estadual',
        max_length=30,
        null=True,
        blank=True,
    )

    razao_social = models.TextField(
        'Razão Social',
        max_length=100,
    )

    nome_fantasia = models.TextField(
        'Nome Fantasia',
        max_length=100,
        null=True,
        blank=True,
    )

    certificado = models.CharField(
        'Certificado',
        max_length=30,
        null=True,
        blank=True,
    )

    simples_nacional = models.BooleanField(
        'Optante do simples nacional?',
        default=False,
    )

    regime_tributario = models.IntegerField(
        'Regime Tributário',
        choices=REGIME_TRIBUTARIO,
    )

    incentivo_fiscal = models.BooleanField(
        'Possui algum tipo de incentivo fiscal?',
        default=False,
    )

    incentivo_cultural = models.BooleanField(
        'É incentivador cultural?',
        default=False,
    )

    regime_tributario_especial = models.IntegerField(
        'Regime tributário adotado pela empresa',
        choices=REGIME_TRIBUTARIO_ESPECIAL,
    )
    
    deletado = models.BooleanField(
        'Deletado?',
        default=False,
    )

    def delete(self):
        self.deletado = True
        self.save()

    def __str__(self):
        return self.razao_social

class Endereco(models.Model):

    empresa = models.OneToOneField(
        'Empresa',
        related_name='endereco',
        on_delete=models.CASCADE,
    )

    tipo_logradouro = models.CharField(
        'Tipo do Logradouro',
        max_length=15,
        choices=TipoLogradouroEnum.choices,
    )

    logradouro = models.CharField(
        'Logradouro',
        max_length=100,
    )

    numero = models.CharField(
        'Número',
        max_length=15,
    )

    complemento = models.CharField(
        'Complemento',
        max_length=50,
        null=True,
        blank=True,
    )

    tipo_bairro = models.CharField(
        'Tipo do Bairro',
        max_length=15,
        choices=TipoBairroEnum.choices,
        null=True,
        blank=True,
    )

    bairro = models.CharField(
        'Nome do Bairro',
        max_length=80,
        null=True,
        blank=True,
    )

    codigo_pais = models.CharField(
        'Código do País',
        max_length=10,
        default='1058',
    )

    descricao_pais = models.CharField(
        'Nome do País',
        max_length=50,
        default='Brasil',
    )

    codigo_cidade = models.CharField(
        'Código IBGE da cidade',
        max_length=8,
    )

    descricao_cidade = models.CharField(
        'Nome da cidade',
        max_length=100,
        null=True,
        blank=True,
    )

    estado = models.CharField(
        'Sigla do Estado',
        max_length=2,
        choices=EstadoEnum.choices,
        null=True,
        blank=True,
    )

    cep = models.CharField(
        'CEP',
        max_length=8,
    )

class Telefone(models.Model):
    empresa = models.ForeignKey(
        'Empresa',
        related_name='telefones',
        on_delete=models.CASCADE,
    )

    ddd = models.CharField(
        'DDD',
        max_length=2,
        null=True,
        blank=True,
    )

    numero = models.CharField(
        'Número de Telefone',
        max_length=14,
        
    )