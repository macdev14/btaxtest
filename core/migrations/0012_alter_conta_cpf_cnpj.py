# Generated by Django 3.2.5 on 2021-12-09 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20211208_1008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conta',
            name='cpf_cnpj',
            field=models.CharField(max_length=20, verbose_name='CPF/CNPJ'),
        ),
    ]
