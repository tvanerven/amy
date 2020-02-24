# Generated by Django 2.2.10 on 2020-02-14 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoemails', '0006_emailtemplate_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='rqjob',
            name='status',
            field=models.CharField(blank=True, default='', help_text='This field is cached from Redis.', max_length=100, verbose_name='Job status'),
        ),
    ]
