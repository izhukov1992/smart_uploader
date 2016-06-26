from django.conf.urls import url
from .views import getFile

urlpatterns = [
    url(r'^download/(?P<file_id>\d+)/$', getFile, name='download'),
]