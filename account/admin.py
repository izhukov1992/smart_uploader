from django.contrib import admin
from .models import UserFile


class UserFileAdmin(admin.ModelAdmin):
    """account.UserFileAdmin"""

    pass


admin.site.register(UserFile, UserFileAdmin)

