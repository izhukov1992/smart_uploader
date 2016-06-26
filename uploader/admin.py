from django.contrib import admin
from .models import StorageFile

# Register physical files model in admin area
admin.site.register(StorageFile, admin.ModelAdmin)
