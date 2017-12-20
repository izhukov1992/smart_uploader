from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
#from django.contrib import auth
#from django.contrib.auth import login
#from django.contrib.auth import authenticate
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import AuthenticationForm
from tornado_websockets.websocket import WebSocket

#from uploader.models import StorageFile
#from uploader.forms import StorageFileForm
#from uploader.utils import getSHA1Digest
from account.models import UserFile


class BaseView(TemplateView):
    """Base template view
    """

    # Define context dictionary
    context = {}

    def get(self, request):
        """Handle GET-query. Render template. Return HTML-page
        """

        return render(request, self.template_name, self.context)


class IndexView(BaseView):
    """User storage view
    """
    
    template_name = 'account_tornado/index.html'

    def get(self, request):
        """Handle GET
        """

        if request.user.is_anonymous:
            return redirect('account:login')
        
        # Call GET handler of base class
        return super(IndexView, self).get(request)


# Make a new instance of WebSocket and automatically add handler '/ws/files' to Tornado handlers
ws_files = WebSocket('/files')

@ws_files.on
def open(socket):
    # Notify all clients about a new connection
    data = [{'username': file.user.username, 'id': file.pk, 'display_name': file.display_name} for file in UserFile.objects.all()]
    ws_files.emit('new_connection', data={'files': data})


@ws_files.on
def message(socket, data):
    # Reply to the client
    socket.emit('message', data)

    # Wow we got a spammer, let's inform the first client :^)
    if 'spam' in data.message:
        # wow
        ws_files[0].emit('got_spam', {
            'message': data.get('message'),
            'socket': socket
        })
