# Generated by Django 5.0.6 on 2024-05-22 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_remove_task_completion_alter_task_task_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completion',
            field=models.BooleanField(default=False),
        ),
    ]
