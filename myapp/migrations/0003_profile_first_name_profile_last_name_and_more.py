# Generated by Django 4.2.6 on 2024-10-01 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="first_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_name",
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="role",
            field=models.CharField(
                choices=[
                    ("default", "Default"),
                    ("moderator", "Moderator"),
                    ("admin", "Admin"),
                ],
                default="default",
                max_length=20,
            ),
        ),
    ]
