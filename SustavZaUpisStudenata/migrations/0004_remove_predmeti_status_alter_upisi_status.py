# Generated by Django 4.0.4 on 2022-06-22 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SustavZaUpisStudenata', '0003_predmeti_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predmeti',
            name='Status',
        ),
        migrations.AlterField(
            model_name='upisi',
            name='Status',
            field=models.CharField(choices=[('Upisan', 'Upisan'), ('Polozen', 'Polozen'), ('Izgubio potpis', 'Izgubio potpis')], default='Upisan', max_length=15),
        ),
    ]
