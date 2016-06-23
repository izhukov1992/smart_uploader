from django.shortcuts import render
from django.views.generic.base import TemplateView
from uploader.forms import StorageFileForm


class BaseView(TemplateView):
    """account.BaseView"""

    context = dict()

    def get(self, request):
        return render(request, self.template_name, self.context)


class IndexView(BaseView):
    """account.IndexView"""
    
    template_name = 'index.html'

    def get(self, request):
        form = StorageFileForm()
        self.context['form'] = form
        return super(IndexView, self).get(request)


class FilesView(BaseView):
    """account.FilesView"""
    
    template_name = 'files.html'

    def get(self, request):
        return super(FilesView, self).get(request)
