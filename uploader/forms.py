from django import forms


class StorageFileForm(forms.Form):
    """uploader.StorageFileForm"""

    file = forms.FileField()