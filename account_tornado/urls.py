from django.conf.urls import url
from .views import IndexView
"""from .views import UploadView
from .views import DeleteView
from .views import JoinView
from .views import LoginView
from .views import logout"""

app_name = 'account_tornado'
urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),                              # Dashboard url (../)
]
