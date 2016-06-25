from django.shortcuts import render
from django.http import HttpResponse
from django.utils.encoding import iri_to_uri
from account.models import UserFile

def getFile(request, file_id):
    file_user = UserFile.objects.get(pk=file_id)
    
    response = HttpResponse(content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="%s"' % iri_to_uri(file_user.display_name)
    
    file_user.file.file.open()
    response.write(file_user.file.file.read())
    file_user.file.file.close()
    return response
