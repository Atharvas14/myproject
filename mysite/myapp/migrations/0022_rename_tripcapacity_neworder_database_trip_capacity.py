# Generated by Django 4.1.7 on 2023-04-19 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_neworder_database_count_neworder_database_locations_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='neworder_database',
            old_name='tripcapacity',
            new_name='trip_capacity',
        ),
    ]
