# Generated by Django 4.0.2 on 2022-03-09 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0010_file_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="file",
            name="cover",
            field=models.FileField(upload_to="files/"),
        ),
    ]
