# Generated by Django 4.2.4 on 2023-08-29 23:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0002_plan_start_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plan',
            old_name='start_date',
            new_name='date',
        ),
    ]
