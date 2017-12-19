from django.conf.urls import url
from .views import IndexView
from .views import UploadView
from .views import DeleteView
from .views import JoinView
from .views import LoginView
from .views import logout

app_name = 'account'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),                              # Dashboard url (../)
    url(r'^upload/$', UploadView.as_view(), name='upload'),                     # Upload url (../upload/)
    url(r'^delete/(?P<file_id>\d+)/$', DeleteView.as_view(), name='delete'),    # Delete url (../delete/<user storage file ID>/)
    url(r'^join/$', JoinView.as_view(), name='join'),                           # Registration url (../join/)
    url(r'^login/$', LoginView.as_view(), name='login'),                        # Login url (../login/)
    url(r'^logout/$', logout, name='logout'),                                   # Logout url (../logout/)
]
