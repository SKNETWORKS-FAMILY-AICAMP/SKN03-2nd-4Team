# Generated by Django 5.1 on 2024-08-16 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='keywordvolume',
            old_name='date2',
            new_name='date',
        ),
    ]
