# Generated by Django 3.2.5 on 2021-09-30 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_servico_conta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servico',
            name='id_integracao',
            field=models.CharField(help_text='Utilizado SOMENTE quando se cadastra previamente um serviço.', max_length=20, verbose_name='Código EXTERNO de integração do serviço'),
        ),
    ]
