from django.db import models


class File(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    path = models.FilePathField("File Path", null=True)
    user_tags = models.CharField(max_length=200, null=True)
    automatic_tags = models.CharField(max_length=200, null=True)
    full_text = models.TextField(blank=True)
    type = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.name
