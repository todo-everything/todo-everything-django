# Generated by Django 4.2.6 on 2023-12-22 22:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="account",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="account",
            name="last_name",
        ),
    ]