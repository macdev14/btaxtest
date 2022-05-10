# Generated by Django 3.2.5 on 2022-05-10 17:55

from django.db import migrations
import django_dnf.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_conta_id_cedente'),
    ]

    operations = [
        migrations.AddField(
            model_name='conta',
            name='bitrix_dominio',
            field=django_dnf.fields.DomainNameField(blank=True, max_length=72, null=True, verbose_name='Dominio Bitrix'),
        ),
    ]
