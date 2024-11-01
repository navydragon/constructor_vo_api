# Generated by Django 4.1.5 on 2024-05-27 12:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('programs', '0010_ministry'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nsi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_name', models.CharField(max_length=2000, null=True)),
                ('start_date', models.CharField(max_length=100, null=True)),
                ('accept_date', models.CharField(max_length=100, null=True)),
                ('accept_number', models.CharField(max_length=100, null=True)),
                ('nsiDate', models.DateField(null=True)),
                ('nsiNumber', models.CharField(max_length=191, null=True)),
                ('nsiEdit', models.CharField(max_length=191, null=True)),
                ('nsiName', models.TextField(null=True)),
                ('nsiApproveName', models.CharField(max_length=191, null=True)),
                ('nsiProtocolDate', models.DateField(null=True)),
                ('nsiCode', models.CharField(max_length=191, null=True)),
                ('nsiPeriod', models.CharField(max_length=191, null=True)),
                ('nsiBasis', models.TextField(null=True)),
                ('nsiAuthors', models.TextField(null=True)),
                ('nsiEditor', models.CharField(max_length=191, null=True)),
                ('nsiCity', models.CharField(max_length=191, null=True)),
                ('nsiYear', models.IntegerField(null=True)),
                ('nsiPages', models.CharField(max_length=200, null=True)),
                ('nsiProtocolNumber', models.CharField(max_length=191, null=True)),
                ('nsiLink', models.TextField(null=True)),
                ('nsiFullName', models.TextField(null=True)),
                ('created_at', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(null=True)),
                ('author_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('nsiMinistry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='programs.ministry')),
                ('type_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='programs.nsitype')),
            ],
        ),
    ]
