# Generated by Django 5.0.2 on 2024-02-13 09:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccessToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=200)),
                ("subdomain", models.CharField(max_length=200)),
                (
                    "created_at",
                    models.DateTimeField(
                        default=datetime.datetime(
                            2024, 2, 13, 9, 52, 56, 723840, tzinfo=datetime.timezone.utc
                        )
                    ),
                ),
            ],
        ),
    ]
