# Generated by Django 4.0.2 on 2022-03-15 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0012_file_created_file_modified_alter_file_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='cover',
            field=models.FileField(upload_to='files/'),
        ),
    ]
