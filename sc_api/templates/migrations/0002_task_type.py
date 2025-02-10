# Generated by Django 5.0.1 on 2025-01-22 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('templates', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='type',
            field=models.CharField(choices=[('W', 'Work'), ('L', 'Leisure'), ('C', 'Chore')], default='W', max_length=1),
            preserve_default=False,
        ),
    ]
