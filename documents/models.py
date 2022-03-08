from django.db import models


class Files_image(models.Model):
    cover = models.ImageField(upload_to="images/")
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Files_invoice(models.Model):
    cover = models.FileField(upload_to="file/")
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Files_receipt(models.Model):
    cover = models.FileField(upload_to="file/")
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name        


class Files_letter(models.Model):
    cover = models.FileField(upload_to="file/")
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name        


class Files_reports(models.Model):
    cover = models.FileField(upload_to="file/")
    name = models.CharField(max_length=30)
    description = models.TextField()
    private = models.BooleanField(default=False)

    def __str__(self):
        return self.name