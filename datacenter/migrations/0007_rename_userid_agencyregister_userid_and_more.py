# Generated by Django 4.0.5 on 2022-10-21 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0006_rename_agencyid_metadata_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agencyregister',
            old_name='userID',
            new_name='userId',
        ),
        migrations.RenameField(
            model_name='metadata',
            old_name='userID',
            new_name='userId',
        ),
        migrations.RenameField(
            model_name='requestreturn',
            old_name='userID',
            new_name='userId',
        ),
    ]
