# Generated by Django 5.0 on 2023-12-07 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todo_description_alter_todo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
