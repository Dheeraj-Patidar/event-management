# Generated by Django 4.2.19 on 2025-02-28 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0010_remove_registeredstudent_event_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="registeredstudent",
            name="event",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="core.event",
            ),
        ),
        migrations.AddField(
            model_name="registeredstudent",
            name="student",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
