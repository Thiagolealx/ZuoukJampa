from django.utils import timezone
from django.db import migrations, models

def get_default_date():
    return timezone.make_aware(timezone.datetime(2024, 4, 16))

class Migration(migrations.Migration):

    dependencies = [
        ('user', '0030_alter_categoria_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='entrada',
            name='data_entrada',
            field=models.DateField(auto_now_add=True, default=get_default_date),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='saida',
            name='data_saida',
            field=models.DateField(auto_now_add=True, default=get_default_date),
            preserve_default=False,
        ),
    ]