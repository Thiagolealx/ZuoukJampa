# Generated by Django 4.1.2 on 2023-05-08 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balanco_geral', '0005_alter_contratos_valor_ct_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contratos',
            name='comprovante',
            field=models.FileField(blank=True, default='', upload_to=''),
        ),
    ]
