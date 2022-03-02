from django.db import models


class Files(models.Model):
    cover = models.FileField(upload_to="file/")
    name = models.CharField(max_length=30)
    owner = models.CharField(max_length=30)

    def __str__(self):
        return self.name
