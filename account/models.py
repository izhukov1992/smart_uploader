from django.db import models
from django.contrib.auth.models import User
from uploader.models import StorageFile


class UserFile(models.Model):
    """
    Model of files in user storage
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)            # Owner
    file = models.ForeignKey(StorageFile, on_delete=models.CASCADE)     # Physical file
    display_name = models.CharField(max_length=255)                     # User version of file name
    
    def __str__(self):
        """
        In string representation show owner and custom file name
        """

        return "%s | %s" % (self.user.username, self.display_name)
