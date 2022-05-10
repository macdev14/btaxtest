# Generated by Django 3.2.5 on 2021-09-07 22:26

import core.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conta',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('nome', models.CharField(max_length=30, verbose_name='Nome')),
                ('razao_social', models.CharField(blank=True, max_length=50, null=True, verbose_name='Razão Social')),
                ('tipo_pessoa', models.CharField(choices=[('F', 'Pessoa Física'), ('J', 'Pessoa Jurídica')], default='F', max_length=1, verbose_name='Tipo de Pessoa')),
                ('cpf_cnpj', models.CharField(max_length=20, unique=True, verbose_name='CPF/CNPJ')),
                ('rg_ie', models.CharField(blank=True, max_length=17, null=True, verbose_name='RG/I.E.')),
                ('im', models.CharField(blank=True, max_length=12, null=True, verbose_name='IM')),
                ('cnae', models.CharField(blank=True, max_length=7, null=True, verbose_name='CNAE')),
                ('regime_tributario', models.CharField(blank=True, choices=[('SN', 'Simples Nacional'), ('RA', 'Regime de Apuração')], max_length=2, null=True, verbose_name='Regime Tributário')),
                ('endereco_cep', models.CharField(max_length=9, verbose_name='CEP')),
                ('endereco_cidade', models.CharField(max_length=100, verbose_name='Cidade')),
                ('endereco_uf', models.CharField(max_length=2, verbose_name='UF')),
                ('endereco_logradouro', models.CharField(max_length=150, verbose_name='Endereço')),
                ('endereco_numero', models.CharField(max_length=10, verbose_name='Número')),
                ('endereco_complemento', models.CharField(blank=True, max_length=50, null=True, verbose_name='Complemento')),
                ('endereco_bairro', models.CharField(max_length=100, verbose_name='Bairro')),
                ('contato_nome', models.CharField(max_length=100, null=True, verbose_name='Nome Contato')),
                ('contato_telefone', models.CharField(max_length=20, verbose_name='Telefone')),
                ('contato_email', models.EmailField(max_length=150, verbose_name='E-mail')),
                ('is_deletado', models.BooleanField(default=False, verbose_name='Deletado?')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('data_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data da Criação')),
                ('data_atualizacao', models.DateTimeField(auto_now=True, verbose_name='Data da Última Atualizacao')),
                ('foto', models.ImageField(blank=True, null=True, upload_to=core.models.profile_foto_upload, verbose_name='Foto')),
                ('nome', models.CharField(max_length=150, null=True, verbose_name='Nome')),
                ('email', models.EmailField(max_length=150, verbose_name='E-mail')),
                ('telefone', models.CharField(blank=True, max_length=18, null=True, verbose_name='Telefone')),
                ('is_redefinicao_senha', models.BooleanField(default=True, verbose_name='Redefinição de senha?')),
                ('is_deletado', models.BooleanField(default=False, verbose_name='Deletado?')),
                ('conta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contas', to='core.conta')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
