from django.core.paginator import Paginator
from django.http import HttpResponseBadRequest, JsonResponse
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers

from wagtail.admin import messages
from wagtail.admin.forms.search import SearchForm
from wagtail.admin.utils import PermissionPolicyChecker, permission_denied, popular_tags_for_model
from wagtail.core.models import Collection
from wagtail.search.backends import get_search_backends

from wagtail.documents.forms import get_document_form, get_document_multi_form
from wagtail.documents.models import get_document_model
from wagtail.documents.permissions import permission_policy

permission_checker = PermissionPolicyChecker(permission_policy)

class TechCardsListView(TemplateView):
    template_name = 'tech_cards.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Техкарты'}]
        return context


    def get(self, request, *args, **kwargs):
        Document = get_document_model()

        # Get documents (filtered by user permission)
        documents = permission_policy.instances_user_has_any_permission_for(
            request.user, ['change', 'delete']
        )

        # Ordering
        if 'ordering' in request.GET and request.GET['ordering'] in ['title', '-created_at']:
            ordering = request.GET['ordering']
        else:
            ordering = '-created_at'
        documents = documents.order_by(ordering)

        # Filter by collection
        current_collection = None
        collection_id = request.GET.get('collection_id')
        if collection_id:
            try:
                current_collection = Collection.objects.get(id=collection_id)
                documents = documents.filter(collection=current_collection)
            except (ValueError, Collection.DoesNotExist):
                pass

        # Search
        query_string = None
        if 'q' in request.GET:
            form = SearchForm(request.GET, placeholder="Search documents")
            if form.is_valid():
                query_string = form.cleaned_data['q']
                documents = documents.search(query_string)
        else:
            form = SearchForm(placeholder="Search documents")

        # Pagination
        paginator = Paginator(documents, per_page=20)
        page_obj = paginator.get_page(request.GET.get('p'))
        print(page_obj)
        collections = permission_policy.collections_user_has_any_permission_for(
            request.user, ['add', 'change']
        )
        if len(collections) < 2:
            collections = None
        else:
            collections = Collection.order_for_display(collections)

        # Create response
        if request.is_ajax():
            return TemplateResponse(request, 'wagtaildocs/documents/results.html', {
                'ordering': ordering,
                'documents': documents,
                'query_string': query_string,
                'is_searching': bool(query_string),
            })
        else:
            return TemplateResponse(request, 'tech_cards.html', {
                'ordering': ordering,
                'documents': documents,
                'query_string': query_string,
                'is_searching': bool(query_string),

                'search_form': form,
                'popular_tags': popular_tags_for_model(Document),
                'user_can_add': permission_policy.user_has_permission(request.user, 'add'),
                'collections': collections,
                'current_collection': current_collection,
            })

    @vary_on_headers('X-Requested-With')
    def post(self, request, *args, **kwargs):
        Document = get_document_model()
        DocumentForm = get_document_form(Document)
        DocumentMultiForm = get_document_multi_form(Document)        

        print('========= add_tech_card =================')
        print(request.FILES)        
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")

        # Build a form for validation
        form = DocumentForm({
            'title': request.FILES['file'].name,
            'collection': request.POST.get('collection'),
        }, {
            'file': request.FILES['file']
        }, user=request.user)

        if form.is_valid():
            # Save it
            doc = form.save(commit=False)
            doc.uploaded_by_user = request.user
            doc.file_size = doc.file.size

            # Set new document file hash
            doc.file.seek(0)
            doc._set_file_hash(doc.file.read())
            doc.file.seek(0)
            doc.save()

            collections = permission_policy.collections_user_has_any_permission_for(
                request.user, ['add', 'change']
            )
            if len(collections) < 2:
                collections = None
            else:
                collections = Collection.order_for_display(collections)

            # Get documents (filtered by user permission)
            documents = permission_policy.instances_user_has_any_permission_for(
                request.user, ['change', 'delete']
            )
            print(documents)
            # Success! Send back an edit form for this document to the user
            return JsonResponse({
                'success': True,
                'documents': [{'title':doc.title, 'file_size':doc.file_size} for doc in documents],
                'collections': collections,                
                'doc_id': int(doc.id),
            })
        else:
            # Validation error
            return JsonResponse({
                'success': False,
                # https://github.com/django/django/blob/stable/1.6.x/django/forms/util.py#L45
                'error_message': '\n'.join(['\n'.join([force_text(i) for i in v]) for k, v in form.errors.items()]),
            })
