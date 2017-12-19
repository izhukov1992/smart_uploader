from django.conf.urls import url
from .views import getFile

app_name = 'uploader'
urlpatterns = [
    url(r'^download/(?P<file_id>\d+)/$', getFile, name='download'), # Download url (../uploader/download/<user storage file ID>/)
]
