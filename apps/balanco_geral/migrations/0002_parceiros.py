# Generated by Django 4.1.2 on 2023-05-05 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('balanco_geral', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parceiros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50)),
                ('uf', models.CharField(max_length=2)),
                ('descricao', models.CharField(blank=True, max_length=300)),
                ('valor', models.FloatField(blank=True)),
                ('comprovante', models.FileField(default='', upload_to='')),
                ('ano', models.CharField(max_length=4)),
            ],
            options={
                'verbose_name': 'Parceiros',
            },
        ),
    ]
