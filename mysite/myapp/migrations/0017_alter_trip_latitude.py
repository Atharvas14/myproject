# Generated by Django 4.1.7 on 2023-04-18 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
    ]
