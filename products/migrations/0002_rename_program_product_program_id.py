# Generated by Django 4.1.5 on 2023-11-05 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="program",
            new_name="program_id",
        ),
    ]