from django.conf.urls import url
from .views import IndexView
from .views import UploadView
from .views import DeleteView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^delete/(?P<file_id>\d+)/$', DeleteView.as_view(), name='delete'),
]
