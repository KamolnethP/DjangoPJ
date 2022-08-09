# Generated by Django 4.0.5 on 2022-08-08 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0003_remove_agencyregister_isadmin_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='agency',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='dataname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='detail',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='email',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='firstname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='lastname',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='objective',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='request',
            name='requestID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]