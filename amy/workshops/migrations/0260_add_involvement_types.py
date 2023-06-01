# Generated by Django 3.2.19 on 2023-05-17 16:53

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("trainings", "0001_initial_create_involvement"),
        ("workshops", "0259_remove_deprecated_training_requirements"),
    ]

    operations = [
        migrations.AddField(
            model_name="trainingprogress",
            name="date",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Date of occurrence",
            ),
        ),
        migrations.AddField(
            model_name="trainingprogress",
            name="involvement_type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="trainings.involvement",
                verbose_name="Type of involvement",
            ),
        ),
        migrations.AddField(
            model_name="trainingrequirement",
            name="involvement_required",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="trainingprogress",
            name="trainee_notes",
            field=models.CharField(
                blank=True, max_length=255, verbose_name="Notes from trainee"
            ),
        ),
    ]
