# Generated by Django 4.0.2 on 2022-03-07 14:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0006_files_image_delete_files_remove_files_invoice_owner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='files_image',
            old_name='descripion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='files_invoice',
            old_name='descripion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='files_letter',
            old_name='descripion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='files_receipt',
            old_name='descripion',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='files_reports',
            old_name='descripion',
            new_name='description',
        ),
    ]
