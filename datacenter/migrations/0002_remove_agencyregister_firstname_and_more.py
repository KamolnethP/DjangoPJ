# Generated by Django 4.0.5 on 2022-08-08 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencyregister',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='agencyregister',
            name='lastname',
        ),
        migrations.AlterField(
            model_name='agencyregister',
            name='userID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
