from random import choices
from django.db import models
from django.contrib.auth import get_user_model
from .validators import validate_file_extension




class File(models.Model):
    class Choices(models.IntegerChoices):
        image = 1
        invoice = 2
        receipt = 3
        letter = 4
        report = 5


    # cover = models.FileField(upload_to="files/")
    cover = models.FileField(upload_to="files/", validators=[validate_file_extension])
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)
    type = models.IntegerField(choices=Choices.choices, default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class Files_image(models.Model):
#     cover = models.ImageField(upload_to="images/")
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     private = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name

# class Files_invoice(models.Model):
#     cover = models.FileField(upload_to="file/")
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     private = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name


# class Files_receipt(models.Model):
#     cover = models.FileField(upload_to="file/")
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     private = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name        


# class Files_letter(models.Model):
#     cover = models.FileField(upload_to="file/")
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     private = models.BooleanField(default=False)
#     user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
#     def __str__(self):
#         return self.name        


# class Files_reports(models.Model):
#     cover = models.FileField(upload_to="file/")
#     name = models.CharField(max_length=30)
#     description = models.TextField()
#     private = models.BooleanField(default=False)

#     def __str__(self):
#         return self.name