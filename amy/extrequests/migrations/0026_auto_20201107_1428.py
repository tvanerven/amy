# Generated by Django 2.2.13 on 2020-11-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extrequests', '0025_auto_20201105_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='selforganisedsubmission',
            name='end',
            field=models.DateField(null=True, verbose_name='Workshop end date'),
        ),
        migrations.AddField(
            model_name='selforganisedsubmission',
            name='start',
            field=models.DateField(help_text='Please provide the dates that your Self-Organised workshop will run.', null=True, verbose_name='Workshop start date'),
        ),
    ]
