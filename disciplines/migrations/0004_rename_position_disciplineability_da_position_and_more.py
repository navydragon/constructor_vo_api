# Generated by Django 4.1.5 on 2023-11-21 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0003_discipline_abilities_discipline_knowledges'),
    ]

    operations = [
        migrations.RenameField(
            model_name='disciplineability',
            old_name='position',
            new_name='da_position',
        ),
        migrations.RenameField(
            model_name='disciplineknowledge',
            old_name='position',
            new_name='dk_position',
        ),
    ]
