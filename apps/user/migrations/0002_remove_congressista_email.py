# Generated by Django 4.2.2 on 2023-06-15 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='congressista',
            name='email',
        ),
    ]
