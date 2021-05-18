# Generated by Django 2.2.18 on 2021-05-18 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workshops', '0243_auto_20210508_1954'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='rolled_to_membership',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='rolled_from_membership', to='workshops.Membership'),
        ),
    ]
