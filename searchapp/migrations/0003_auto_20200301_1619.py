# Generated by Django 2.1.7 on 2020-03-01 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('searchapp', '0002_file_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='automatic_tags',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='file',
            name='user_tags',
            field=models.CharField(max_length=200),
        ),
    ]