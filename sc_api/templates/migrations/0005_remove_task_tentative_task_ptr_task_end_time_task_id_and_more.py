# Generated by Django 5.0.1 on 2025-02-09 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0004_remove_task_end_time_remove_task_id_remove_task_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='tentative_task_ptr',
        ),
        migrations.AddField(
            model_name='task',
            name='end_time',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='id',
            field=models.AutoField(default=None, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='templates.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='start_time',
            field=models.DateTimeField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('W', 'Work'), ('L', 'Leisure'), ('E', 'Exercise')], default=None, max_length=1),
            preserve_default=False,
        ),
    ]
