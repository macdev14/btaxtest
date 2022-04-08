# Generated by Django 3.2.5 on 2021-09-27 01:37

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20210917_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cofins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_calculo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Base de cálculo do {} Retido')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Alíquota {} retido')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor {} retido')),
                ('cst', models.CharField(max_length=10, verbose_name='Para NFS-e de Brasília: Controla o CST utilizado para emissão da NF-e, por padrão, para optantes do simples nacional, utilizamos 99, para não optantes, utilizamos 01')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cpp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota {} retido')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor {} retido, caso você não informe esse campo, vamos calcular automaticamente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Csll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota {} retido')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor {} retido, caso você não informe esse campo, vamos calcular automaticamente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Deducao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.IntegerField(choices=[(0, 'Sem Deduções'), (1, 'Materiais'), (2, 'Subempreitada de Mão de Obra'), (3, 'Serviços'), (4, 'Produção Externa'), (5, 'Alimentação e Bebidas'), (6, 'Reembolso de Despesas'), (7, 'Repasse Consorciado'), (8, 'Repasse Plano de Saúde'), (99, 'Outras Deduções')], verbose_name='Tipo de Dedução')),
                ('descricao', models.CharField(max_length=512, verbose_name='Descrição da Dedução')),
            ],
        ),
        migrations.CreateModel(
            name='Ibpt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='IbptDetalhado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliquota_municipal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota municipal de impostos')),
                ('aliquota_estadual', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota estadual de impostos')),
                ('aliquota_federal', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota federal de impostos')),
            ],
        ),
        migrations.CreateModel(
            name='IbptSimplificado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota Geral de Impostos')),
            ],
        ),
        migrations.CreateModel(
            name='Inss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota {} retido')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor {} retido, caso você não informe esse campo, vamos calcular automaticamente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Irrf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota {} retido')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor {} retido, caso você não informe esse campo, vamos calcular automaticamente')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Iss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_tributacao', models.IntegerField(choices=[(1, 'Isento de ISS'), (2, 'Imune'), (3, 'Não Incidência no Município'), (4, 'Não Tributável'), (5, 'Retido'), (6, 'Tributável Dentro do Município'), (7, 'Tributável Fora do Município'), (8, 'Tributável Dentro do Município pelo tomador')], default=6, verbose_name='Tipo de Tributação do Serviço')),
                ('exigibilidade', models.IntegerField(choices=[(1, 'Exigível'), (2, 'Não Incidência'), (3, 'Isenção'), (4, 'Exportação'), (5, 'Imunidade'), (6, 'Suspenso por Ação Judicial'), (7, 'Suspenso por Ação Administrativa')], default=1, verbose_name='Exigibilidade do ISS')),
                ('retido', models.BooleanField(default=False, verbose_name='Reter ISS')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Aliquota do ISS do serviço prestado')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor do ISS')),
                ('valor_retido', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor ISS retido')),
                ('processo_suspensao', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numero do Processo de Suspensão da Exigibilidade')),
            ],
        ),
        migrations.CreateModel(
            name='Obra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('art', models.CharField(max_length=20, verbose_name='Código do ART')),
                ('codigo', models.CharField(max_length=10, verbose_name='Código da Obra (CO)')),
                ('cei', models.CharField(max_length=10, verbose_name='Cadastro específico do INSS')),
            ],
        ),
        migrations.CreateModel(
            name='Pis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_calculo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Base de cálculo do {} Retido')),
                ('aliquota', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Alíquota {} retido')),
                ('valor', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor {} retido')),
                ('cst', models.CharField(max_length=10, verbose_name='Para NFS-e de Brasília: Controla o CST utilizado para emissão da NF-e, por padrão, para optantes do simples nacional, utilizamos 99, para não optantes, utilizamos 01')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Retencao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('outras_retencoes', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor de outras retenções')),
                ('cofins', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.cofins')),
                ('cpp', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.cpp')),
                ('csll', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.csll')),
                ('inss', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.inss')),
                ('irrf', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.irrf')),
                ('pis', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.pis')),
            ],
        ),
        migrations.CreateModel(
            name='Valor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_calculo', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor da base de cálculo dos impostos')),
                ('deducoes', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor deduções')),
                ('desconto_condicionado', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor do desconto condicionado')),
                ('desconto_incondicionado', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor do desconto incondicionado')),
                ('liquido', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor líquido do serviço')),
                ('unitario', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor unitário do serviço')),
                ('valor_aproximado_tributos', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor aproximado dos tributos. Campo utilizado somente para NFS-e de Brasília')),
            ],
        ),
        migrations.CreateModel(
            name='Servico',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Id')),
                ('codigo', models.CharField(max_length=10, verbose_name='Código')),
                ('id_integracao', models.CharField(max_length=20, verbose_name='Código EXTERNO de integração do serviço. Utilizado SOMENTE quando se cadastra previamente um serviço.')),
                ('discriminacao', models.CharField(max_length=1024, verbose_name='Detalhamento do serviço prestado')),
                ('codigo_tributacao', models.CharField(max_length=10, verbose_name='Código tributação no Município')),
                ('cnae', models.CharField(max_length=512, verbose_name='CNAE')),
                ('codigo_cidade_incidencia', models.CharField(max_length=10, verbose_name='Codigo IBGE da cidade de incidência do ISS')),
                ('descricao_cidade_incidencia', models.CharField(max_length=100, verbose_name='Nome da cidade de incidência do ISS')),
                ('unidade', models.CharField(max_length=10, verbose_name='Unidade de serviço prestado')),
                ('quantidade', models.IntegerField(verbose_name='Quantidade dos serviços prestados')),
                ('tributavel', models.BooleanField(default=False, verbose_name='Serviço sujeito a triutação')),
                ('responsavel_retencao', models.IntegerField(choices=[(1, 'Tomador'), (2, 'Intermediário')], verbose_name='Responsável Retenção')),
                ('tributos_federais_retidos', models.BooleanField(default=True, verbose_name='Tributos Federais Retidos')),
                ('deletado', models.BooleanField(default=False, verbose_name='Deletado?')),
                ('deducao', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.deducao')),
                ('ibpt', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.ibpt')),
                ('iss', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.iss')),
                ('obra', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.obra')),
                ('retencao', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.retencao')),
                ('valor', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.valor')),
            ],
        ),
        migrations.AddField(
            model_name='ibpt',
            name='detalhado',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.ibptdetalhado'),
        ),
        migrations.AddField(
            model_name='ibpt',
            name='simplificado',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.ibptsimplificado'),
        ),
    ]
