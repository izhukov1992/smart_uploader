from django.db import models


class StorageFile(models.Model):
    """Model of physical files
    """

    file = models.FileField()                               # Relative path to file
    sha1 = models.CharField(max_length=255, unique=True)    # Hash of file
    
    def __str__(self):
        """In string representation show relative path to file
        """

        return str(self.file)
