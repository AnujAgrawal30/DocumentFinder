# Generated by Django 3.0.3 on 2020-02-08 11:49

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('path', models.FilePathField(verbose_name='File Path')),
                ('user_tags', django_mysql.models.ListCharField(models.CharField(max_length=20), max_length=210, size=10)),
                ('automatic_tags', django_mysql.models.ListCharField(models.CharField(max_length=20), max_length=210, size=10)),
                ('full_text', models.TextField(blank=True)),
            ],
        ),
    ]
