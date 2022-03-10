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


    def get_cover(self):
        try:
            if self.cover:
                print(self.cover.url)
                return "localhost:8000" + str(self.cover.url)
            else:
                return ""
        except NameError:
            return ""