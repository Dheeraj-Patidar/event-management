# Generated by Django 4.2.19 on 2025-02-28 06:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0011_registeredstudent_event_registeredstudent_student"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="registeredstudent",
            name="event",
        ),
        migrations.RemoveField(
            model_name="registeredstudent",
            name="student",
        ),
    ]
