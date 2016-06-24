from django.contrib import admin
from .models import StorageFile


class StorageFileAdmin(admin.ModelAdmin):
    """uploader.StorageFileAdmin"""

    pass


admin.site.register(StorageFile, StorageFileAdmin)
