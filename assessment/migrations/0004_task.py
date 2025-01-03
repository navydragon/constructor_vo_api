# Generated by Django 5.0.6 on 2024-11-07 08:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0003_answer_position_answer_text2'),
        ('competenceprofile', '0010_knowledge_abilities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('ability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='competenceprofile.ability')),
            ],
        ),
    ]
