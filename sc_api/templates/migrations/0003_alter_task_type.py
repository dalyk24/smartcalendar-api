# Generated by Django 5.0.1 on 2025-02-04 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0002_task_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('W', 'Work'), ('L', 'Leisure'), ('E', 'Exercise')], max_length=1),
        ),
    ]
