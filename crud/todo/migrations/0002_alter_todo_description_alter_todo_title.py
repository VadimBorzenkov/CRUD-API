# Generated by Django 5.0 on 2023-12-07 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
