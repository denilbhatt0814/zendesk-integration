# Generated by Django 5.0.2 on 2024-02-19 16:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zendesk", "0005_ticket_assignee_email_ticket_assignee_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="satisfaction_rating",
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
