# Generated by Django 5.0.6 on 2025-01-16 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0008_semesterdiscipline_zet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semesterdiscipline',
            name='control',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
