# Generated by Django 4.2.19 on 2025-02-28 05:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0009_alter_registeredstudent_enrolled_date"),
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
