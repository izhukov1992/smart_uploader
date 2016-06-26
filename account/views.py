from django.shortcuts import render
from django.shortcuts import redirect
from django.core.context_processors import csrf
from django.views.generic.base import TemplateView
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from uploader.models import StorageFile
from uploader.forms import StorageFileForm
from uploader.utils import getSHA1Digest
from .models import UserFile


class BaseView(TemplateView):
    """account.BaseView"""

    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)


class IndexView(BaseView):
    """account.IndexView"""
    
    template_name = 'index.html'

    def get(self, request):
        if request.user.is_anonymous():
            return redirect('account:login')
        
        files = UserFile.objects.filter(user=request.user)
        self.context.update({'files': files})
        
        form = StorageFileForm()
        self.context.update(csrf(request))
        self.context.update({'form': form})
        
        return super(IndexView, self).get(request)


class UploadView(BaseView):
    """account.UploadView"""
    
    template_name = 'upload.html'

    def post(self, request):
        if request.user.is_anonymous():
            return redirect('account:login')

        if UserFile.objects.filter(user=request.user).count() > 99:
            self.context.update({'limit': True})
            return super(UploadView, self).get(request)

        form = StorageFileForm(request.POST, request.FILES)
        if not form.is_valid():
            self.context.update({'form': form})
            return super(UploadView, self).get(request)

        file_uploaded = request.FILES['file']
        hash = getSHA1Digest(file_uploaded)
        try:
            file_duplicate = StorageFile.objects.get(sha1=hash)
        except:
            file_duplicate = None
        if file_duplicate:
            self.context.update({'file_duplicate': file_duplicate})
            file_new = file_duplicate
        else:
            file_new = StorageFile(file=file_uploaded, sha1=hash)
            file_new.save()

        file_user = UserFile(user=request.user, file=file_new, display_name=file_uploaded)
        file_user.save()
        self.context.update({'file_new': file_user})

        return super(UploadView, self).get(request)


class DeleteView(BaseView):
    """account.DeleteView"""
    
    template_name = 'delete.html'

    def get(self, request, file_id):
        if request.user.is_anonymous():
            return redirect('account:login')

        file_user = UserFile.objects.get(pk=file_id)
        file_storage = file_user.file
        file_user.delete()
        if file_storage.userfile_set.count() < 1:
            file_storage.file.delete()
            file_storage.delete()
        return super(DeleteView, self).get(request)


class LoginView(BaseView):
    """account.LoginView"""
    
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated():
            return redirect('account:index')

        form = AuthenticationForm()
        self.context.update(csrf(request))
        self.context.update({'form': form})
        return super(LoginView, self).get(request)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('account:index')
        return super(LoginView, self).get(request)

def logout(request):
    auth.logout(request)
    return redirect('account:login')
