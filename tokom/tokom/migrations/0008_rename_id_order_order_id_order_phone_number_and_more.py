# Generated by Django 5.0.4 on 2024-11-27 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokom", "0007_alter_order_address"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="id",
            new_name="order_id",
        ),
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name="orderdetail",
            name="price_per_item",
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[("ongoing", "Ongoing"), ("finished", "Finished")],
                default="ongoing",
                max_length=10,
            ),
        ),
    ]
