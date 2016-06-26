from django.db import models


class StorageFile(models.Model):
    """uploader.StorageFile"""

    file = models.FileField()
    sha1 = models.CharField(max_length=255, unique=True)
