from django.conf.urls import url
from .views import IndexView
from .views import UploadView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
]
