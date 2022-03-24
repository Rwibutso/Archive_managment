# Generated by Django 4.0.2 on 2022-03-09 18:32

from django.db import migrations, models
import documents.validators


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0011_alter_file_cover"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, default="2021-12-31 15:25:00+01"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="file",
            name="modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="file",
            name="cover",
            field=models.FileField(
                upload_to="files/",
                validators=[documents.validators],
            ),
        ),
    ]