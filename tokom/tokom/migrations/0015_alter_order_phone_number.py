# Generated by Django 5.0.4 on 2024-11-29 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokom", "0014_order_date_arrived_order_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="phone_number",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
