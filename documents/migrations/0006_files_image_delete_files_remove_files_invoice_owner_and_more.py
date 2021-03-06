# Generated by Django 4.0.2 on 2022-03-07 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("documents", "0005_files_invoice_files_letter_files_receipt_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Files_image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cover", models.ImageField(upload_to="images/")),
                ("name", models.CharField(max_length=30)),
                ("descripion", models.TextField()),
                ("private", models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name="Files",
        ),
        migrations.RemoveField(
            model_name="files_invoice",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="files_letter",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="files_receipt",
            name="owner",
        ),
        migrations.RemoveField(
            model_name="files_reports",
            name="owner",
        ),
        migrations.AddField(
            model_name="files_invoice",
            name="descripion",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="files_letter",
            name="descripion",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="files_receipt",
            name="descripion",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="files_reports",
            name="descripion",
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
