from django.contrib import admin
from .models import StorageFile

admin.site.register(StorageFile, admin.ModelAdmin)
