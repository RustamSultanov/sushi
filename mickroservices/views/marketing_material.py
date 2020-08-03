from django.http import HttpResponseBadRequest, JsonResponse
from django.views.generic import ListView
from django.views.decorators.vary import vary_on_headers
from django.utils.encoding import force_text
from wagtail.documents.forms import get_document_form
from wagtail.documents.permissions import permission_policy

from mickroservices.models import MarketingMaterial
from mickroservices.models import DocumentSushi, DocumentPreview
from mickroservices.utils import FileConverter

from os import path
from django.conf import settings



def get_marketing_documents(doc_type=4):
    documents = DocumentSushi.objects.filter(doc_type=doc_type)
    return documents

class MarketingView(ListView):
    template_name = 'marketingmaterial.html'
    model = MarketingMaterial
    paginate_by = 9
    context_object_name = 'materials'

    def get_context_data(self, **kwargs):
        context = super(MarketingView, self).get_context_data(**kwargs)

        context['types_marketing'] =MarketingMaterial.TYPE_CHOICE
        context['breadcrumb'] = [{'title': 'Маркетинговые материалы'}]
        #context['documents'] = get_marketing_documents()
        context['active_tab'] = MarketingMaterial.T_PROMOTIONS
        return context

    def verife_http_response(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")
        return None

    def get_doc_form(self, request):
        # Build a form for validation
        DocumentForm = get_document_form(DocumentSushi)
        return DocumentForm(
            {
                "title": request.FILES["file"].name,
                "collection": request.POST.get("collection"),
            },
            {"file": request.FILES["file"]},
            user=request.user,
        )

    def save_doc(self,request, doc, doc_type):
        doc.doc_type = doc_type
        doc.uploaded_by_user = request.user
        doc.file_size = doc.file.size

        # Set new document file hash
        doc.file.seek(0)
        doc._set_file_hash(doc.file.read())
        doc.file.seek(0)
        doc.save()

        self.generate_doc_preview(doc.id)

    def generate_doc_preview(self, id_):
        self._generate_doc_preview(id_)
        
    def _generate_doc_preview(self, id_):
        doc = DocumentSushi.objects.get(pk=id_)
        filename = doc.file.name
        source_path = path.join(settings.MEDIA_ROOT, filename)
        ext = filename.split('.')[-1].lower()
        
        available_types = ('docx', 'doc', 'ppt', 'pptx')

        if ext == 'pdf':
            return 

        if ext in available_types:
            target_filename = filename.split('.')[0] + '_preview.pdf'
            target_path = path.normpath(path.join(settings.MEDIA_ROOT, target_filename))
            
            converter = FileConverter()
            if converter.convert(ext, 'pdf', source_path, target_path):
                preview = DocumentPreview(file=target_path,
                                          title=target_filename,
                                          wagtail_document=id_)

                preview.save()


    @vary_on_headers("X-Requested-With")
    def post(self, request, *args, **kwargs):

        respone = self.verife_http_response(request)
        if respone:
            return respone

        form = self.get_doc_form(request)

        if form.is_valid():
            # Save it
            doc = form.save(commit=False)

            doc_type = request.POST.get("type")

            self.save_doc(request, doc, doc_type)

            return JsonResponse({"success": True})
        else:
            # Validation error
            return JsonResponse(
                {
                    "success": False,
                    "error_message": "\n".join(
                        [
                            "\n".join([force_text(i) for i in v])
                            for k, v in form.errors.items()
                        ]
                    ),
                }
            )
