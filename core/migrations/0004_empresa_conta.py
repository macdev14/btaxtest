# Generated by Django 3.2.5 on 2021-09-13 13:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_empresa_deletado'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='conta',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to='core.conta'),
            preserve_default=False,
        ),
    ]
