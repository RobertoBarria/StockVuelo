# Generated by Django 5.0.4 on 2024-05-30 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='avion',
            name='descripcion',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='stockavion',
            name='cantidad_Minima',
            field=models.IntegerField(default=0),
        ),
    ]
