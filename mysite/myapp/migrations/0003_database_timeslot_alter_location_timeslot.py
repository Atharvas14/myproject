# Generated by Django 4.1.7 on 2023-03-16 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_database'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='timeslot',
            field=models.CharField(default='9:00am - 5:00pm', max_length=50),
        ),
        migrations.AlterField(
            model_name='location',
            name='timeslot',
            field=models.CharField(max_length=50),
        ),
    ]
