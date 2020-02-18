# Generated by Django 2.2.10 on 2020-02-18 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autoemails', '0007_rqjob_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='rqjob',
            name='event_slug',
            field=models.CharField(blank=True, default='', help_text="Related event's slug.", max_length=100, verbose_name='Event slug'),
        ),
        migrations.AddField(
            model_name='rqjob',
            name='mail_status',
            field=models.CharField(blank=True, default='', help_text='This field is updated from Mailgun.', max_length=100, verbose_name='Mail status'),
        ),
        migrations.AddField(
            model_name='rqjob',
            name='recipients',
            field=models.CharField(blank=True, default='', max_length=300, verbose_name='Mail recipients'),
        ),
    ]
