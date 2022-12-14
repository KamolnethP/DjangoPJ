# Generated by Django 4.0.5 on 2022-11-09 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datacenter', '0009_alter_metadata_datasetgroupid_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MetaDataMapField',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('metadataId', models.IntegerField()),
                ('metadataGroupId', models.IntegerField()),
                ('fieldNameUser', models.CharField(max_length=255)),
                ('dataTypeField', models.CharField(max_length=20, null=True)),
                ('discription', models.TextField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='metadata',
            name='stopWord',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='dataSetGroupId',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='metadata',
            name='metadataGroupId',
            field=models.IntegerField(),
        ),
    ]
