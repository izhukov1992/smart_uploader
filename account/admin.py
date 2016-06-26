from django.contrib import admin
from .models import UserFile

# Register user storage files in admin area
admin.site.register(UserFile, admin.ModelAdmin)
