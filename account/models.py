from django.db import models
from django.contrib.auth.models import User
from uploader.models import StorageFile


class UserFile(models.Model):
    """account.UserFile"""

    user = models.ForeignKey(User)
    file = models.ForeignKey(StorageFile)
    display_name = models.CharField(max_length=255)
    
    def __str__(self):
        return "%s | %s" % (self.user.username, self.display_name)
