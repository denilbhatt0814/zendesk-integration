# Generated by Django 5.0.2 on 2024-02-19 16:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zendesk", "0007_ticket_subdomain"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="ticket_id",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="ticket",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ticket",
            unique_together={("ticket_id", "subdomain")},
        ),
    ]