# Generated by Django 3.1.2 on 2020-11-22 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0007_obligations'),
    ]

    operations = [
        migrations.RenameField(
            model_name='obligations',
            old_name='quantum',
            new_name='kwota',
        ),
    ]
