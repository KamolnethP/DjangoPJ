# Generated by Django 4.0.5 on 2022-10-21 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0005_file_filename'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metadata',
            old_name='agencyId',
            new_name='userID',
        ),
    ]
