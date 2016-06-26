from django.conf.urls import url
from .views import IndexView
from .views import UploadView
from .views import DeleteView
from .views import JoinView
from .views import LoginView
from .views import logout

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^upload/$', UploadView.as_view(), name='upload'),
    url(r'^delete/(?P<file_id>\d+)/$', DeleteView.as_view(), name='delete'),
    url(r'^join/$', JoinView.as_view(), name='join'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout, name='logout'),
]
