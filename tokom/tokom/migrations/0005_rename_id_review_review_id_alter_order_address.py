# Generated by Django 5.0.4 on 2024-11-25 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tokom", "0004_alter_item_image"),
    ]

    operations = [
        migrations.RenameField(
            model_name="review",
            old_name="id",
            new_name="review_id",
        ),
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.CharField(max_length=255, null=True),
        ),
    ]