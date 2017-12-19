from django import forms


class StorageFileForm(forms.Form):
    """File uploading form
    """

    file = forms.FileField()    # File from computer