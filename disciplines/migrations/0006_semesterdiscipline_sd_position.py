# Generated by Django 4.1.5 on 2023-12-12 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disciplines', '0005_semester_semesterdiscipline_semester_disciplines_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='semesterdiscipline',
            name='sd_position',
            field=models.IntegerField(default=0),
        ),
    ]
