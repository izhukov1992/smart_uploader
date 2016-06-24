from django.shortcuts import render
from django.core.context_processors import csrf
from django.views.generic.base import TemplateView
from uploader.models import StorageFile
from uploader.forms import StorageFileForm
from uploader.utils import getSHA1Digest


class BaseView(TemplateView):
    """account.BaseView"""

    context = {}

    def get(self, request):
        return render(request, self.template_name, self.context)


class IndexView(BaseView):
    """account.IndexView"""
    
    template_name = 'index.html'

    def get(self, request):
        self.context = {}
        form = StorageFileForm()
        self.context.update(csrf(request))
        self.context.update({'form': form})
        return super(IndexView, self).get(request)

    def post(self, request):
        form = StorageFileForm(request.POST, request.FILES)
        if not form.is_valid():
            self.context.update({'form': form})
            return super(IndexView, self).get(request)
            
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
            self.context.update({'file_new': file_new})
        #user area file instance creation
        return super(IndexView, self).get(request)


class FilesView(BaseView):
    """account.FilesView"""
    
    template_name = 'files.html'

    def get(self, request):
        return super(FilesView, self).get(request)
