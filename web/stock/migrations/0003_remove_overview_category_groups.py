# Generated by Django 2.1 on 2018-09-21 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_overview_category_groups'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='overview',
            name='category_groups',
        ),
    ]
