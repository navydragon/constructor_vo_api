# Generated by Django 4.1.5 on 2023-11-08 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_program'),
        ('programs', '0007_programuser_program_id_programuser_role_id_and_more'),
        ('competenceprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Knowledge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('position', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('abilities', models.ManyToManyField(related_name='knowledges', to='products.process')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='knowledges', to='programs.program')),
            ],
            options={
                'db_table': 'knowledges',
            },
        ),
    ]
