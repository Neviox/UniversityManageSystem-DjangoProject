# Generated by Django 4.0.4 on 2022-06-22 19:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('SustavZaUpisStudenata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='predmeti',
            name='NositeljKolegija',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Nositelj', to=settings.AUTH_USER_MODEL),
        ),
    ]
