from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
#from django.contrib import auth
#from django.contrib.auth import login
#from django.contrib.auth import authenticate
#from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.forms import AuthenticationForm
#from uploader.models import StorageFile
from uploader.forms import StorageFileForm
#from uploader.utils import getSHA1Digest
from account.models import UserFile
from tornado_websockets.websocket import WebSocket

# Make a new instance of WebSocket and automatically add handler '/ws/my_ws' to Tornado handlers
ws_echo = WebSocket('/echo')

@ws_echo.on
def open(socket):
    # Notify all clients about a new connection
    ws_echo.emit('new_connection')

@ws_echo.on
def message(socket, data):
    # Reply to the client
    socket.emit('message', data)

    # Wow we got a spammer, let's inform the first client :^)
    if 'spam' in data.message:
        # wow
        ws_echo[0].emit('got_spam', {
            'message': data.get('message'),
            'socket': socket
        })

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

        # Find all files in user storage 
        files = UserFile.objects.filter(user=request.user)
        # Update context
        self.context.update({'files': files})
        
        # Create file uploading form
        form = StorageFileForm()
        # Update context
        self.context.update({'form': form})
        
        # Call GET handler of base class
        return super(IndexView, self).get(request)
