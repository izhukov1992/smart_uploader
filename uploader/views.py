from django.http import HttpResponse
from django.utils.encoding import iri_to_uri
from account.models import UserFile


def getFile(request, file_id):
    """Download view
    """

    # Find user storage file by ID
    file_user = UserFile.objects.get(pk=file_id)

    # Prepare HTTP header to return byte stream
    response = HttpResponse(content_type='application/octet-stream')
    # Prepare HTTP header to return attachment with custom file name
    response['Content-Disposition'] = 'attachment; filename="%s"' % iri_to_uri(file_user.display_name)
    
    # Get physical file by foreign key and open
    with file_user.file.file as file:
        # Write byte stream to response object
        response.write(file.read())

    return response
