# Generated by Django 3.0.8 on 2020-10-02 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_client_player_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='cpf_cnpj',
            field=models.CharField(max_length=14, null=True, verbose_name='CPF/CNPJ'),
        ),
    ]
