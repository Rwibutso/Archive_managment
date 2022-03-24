from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
# from .validators import validate_file_extension
# from .validators import validate_file_extension
from rest_framework.exceptions import ValidationError
import os

class File(models.Model):
    class Choices(models.IntegerChoices):
        image = 1
        invoice = 2
        receipt = 3
        letter = 4
        report = 5

    cover = models.FileField(upload_to="files/")
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)
    type = models.IntegerField(choices=Choices.choices, default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        ext = os.path.splitext(self.cover.name)[1]
        valid_extensions_image = ['.png','.jpeg','.svg']
        valid_extensions_invoice = ['.pdf','.doc','.docs','.ppt','.txt']
        valid_extensions_letter = ['.pdf','.doc','.docs','.ppt','.txt']
        valid_extensions_receipts = ['.pdf','.doc','.docs','.ppt','.txt']
        valid_extensions_reports = ['.pdf','.doc','.docs','.ppt','.txt']
        if self.type == 1:
            if not ext.lower() in valid_extensions_image:
                raise ValidationError("only images allowed")

        if self.type == 2:
            if not ext.lower() in valid_extensions_invoice:
                raise ValidationError("Unsupported file extension")

        if self.type == 3:
            if not ext.lower() in valid_extensions_letter:
                raise ValidationError("Unsupported file extension")

        if self.type == 4:
            if not ext.lower() in valid_extensions_receipts:
                raise ValidationError("Unsupported file extension")


        if self.type == 5:
            if not ext.lower() in valid_extensions_reports:
                raise ValidationError("Unsupported file extension")
        super(File, self).save(*args, **kwargs)


    def get_cover(self):
        try:
            if self.cover:
                print(self.cover.url)
                return "http://localhost:8000" + str(self.cover.url)
            else:
                return ""
        except NameError:
            return ""


