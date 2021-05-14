import os


from django.http import FileResponse
from django.conf import settings
from django.shortcuts import render, Http404
from django.shortcuts import get_object_or_404


from .models import FilesMailing, Mailing


def download_mail_files(request):
    " download onli mailing files"

    try:
        path = request.GET['path']
        dirs = FilesMailing.file.field.upload_to.split('/')[0]
        if path.split('/')[0] == dirs:
            file_path = os.path.join(settings.MEDIA_ROOT, path)
            return FileResponse(open(file_path, 'rb'))
    except :
        raise Http404
    raise Http404


# def single_view(request,pk,*args,**kwargs):
#     obj = get_object_or_404(Mailing,pk=pk)
#     return render(request, "mailing/single_view.html", {"obj": obj})
