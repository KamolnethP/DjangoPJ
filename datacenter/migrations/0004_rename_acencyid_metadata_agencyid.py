# Generated by Django 4.0.5 on 2022-10-19 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0003_agency_remove_agencyregister_agency_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='metadata',
            old_name='acencyId',
            new_name='agencyId',
        ),
    ]