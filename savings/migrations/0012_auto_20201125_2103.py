# Generated by Django 3.1.2 on 2020-11-25 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('savings', '0011_auto_20201125_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneybox',
            name='wolumen',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='obligations',
            name='kwota',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='outgoings',
            name='suma',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='yourgoal',
            name='cel',
            field=models.IntegerField(),
        ),
    ]