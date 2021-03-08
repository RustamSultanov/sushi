from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.decorators.vary import vary_on_headers

try:
    from wagtail.admin.utils import user_passes_test
except ImportError:
    from wagtail.admin.auth import user_passes_test
from wagtail.users.forms import AvatarPreferencesForm
import wagtail.users.models
from django.http import (HttpResponse,
                         HttpResponseBadRequest, JsonResponse, HttpResponseRedirect)
from django.views.generic import ListView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import force_text
from wagtail.admin.forms.search import SearchForm
from wagtail.core.models import Collection
from wagtail.documents.forms import get_document_form
from wagtail.documents.permissions import permission_policy
from django.contrib.auth.models import Group
from django.forms import modelformset_factory
from django.template.loader import render_to_string

from chat.models import Message as Chat_Message
from mickroservices.models import DocumentPreview
from mickroservices.forms import AnswerForm, IdeaStatusForm
from mickroservices.consts import *
from .forms import *
from .models import *
from .enums import *
from .signals import handle_materials

import json
import pandas as pd
import secrets

User = get_user_model()


@csrf_exempt
def delete_directory(request):
    directory = Directory.objects.get(id=request.POST["DIR_ID"])
    directory.delete()
    return JsonResponse({'success': True})


@csrf_exempt
def delete_directory_file(request):
    dir_file = DirectoryFile.objects.get(id=request.POST["FILE_ID"])
    dir_file.delete()
    return JsonResponse({'success': True})


@csrf_exempt
def show_directories(request):
    node = Directory.objects.get(id=request.POST["PARENT_ID"])
    user = UserProfile.objects.get(user=request.user)
    response = render_to_string('directories.html', {'node': node, 'user': user})
    return JsonResponse({'success': True, 'response': response})


@csrf_exempt
def add_directory_file(request):
    directory = Directory.objects.get(id=request.POST["PARENT_ID"])
    dir_file = DirectoryFile.objects.create(directory=directory, dir_file=request.FILES["file"])
    is_manager = False
    user = UserProfile.objects.get(user=request.user)
    if user.is_manager:
        is_manager = True
    return JsonResponse({'success': True, 'dir_file_url': dir_file.dir_file.url, 'dir_file_name': dir_file.filename(),
                         'is_manager': is_manager, 'dir_file_id': dir_file.id})


@csrf_exempt
def add_directory(request):
    title = request.POST.get('TITLE', '')
    parent_id = request.POST.get('PARENT_ID', '')
    dir = Directory.objects.create(parent_id=parent_id, title=title)
    is_manager = False
    user = UserProfile.objects.get(user=request.user)
    if user.is_manager:
        is_manager = True
    return JsonResponse({'success': True, 'dir_title': dir.title, 'dir_id': dir.id, 'is_manager': is_manager})


def get_filtered_shop_feedback(request, shop_id):
    feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
        shop=shop_id
    )
    if "filter_feedback" in request.GET:
        return feedback_list.filter(status=request.GET['filter_feedback'])
    return feedback_list


@csrf_exempt
def load_filtered_shop_feedback(request, shop_id):
    feedback_list = get_filtered_shop_feedback(request, shop_id)
    return render(
        request,
        'partials/feedback_manager.html',
        {'feedback_list': feedback_list}
    )


class ShopListView(ListView):
    model = DocumentSushi
    paginate_by = 9
    context_object_name = "documents"
    template_name = "store.html"

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def get_context_data(self, **kwargs):
        shop = get_object_or_404(Shop, id=self.kwargs["shop_id"])
        context = super().get_context_data(**kwargs)
        context["invoices"] = self.get_invoices()
        context["shop"] = shop
        context["shop_sign"] = ShopSign.objects.all()
        context["feedback_list"] = get_filtered_shop_feedback(self.request, self.kwargs["shop_id"])
        context["doc_type"] = DocumentSushi.T_PERSONAL
        context["type_invoice"] = DocumentSushi.T_PERSONAL_INVOICES
        context["breadcrumb"] = [
            {"title": "Личный кабинет", "url": reverse_lazy("partner_lk")},
            {"title": f"Магазин #{shop.id}"},
        ]
        return context

    def get_documents(self):
        shop = Shop.objects.get(id=self.kwargs["shop_id"])
        documents = shop.docs.all().order_by("title")
        return documents

    def get_invoices(self):
        shop = Shop.objects.get(id=self.kwargs["shop_id"])
        return shop.checks.all().order_by("title")

    def get_queryset(self):
        # Get documents (filtered by user permission)
        documents = self.get_documents()
        invoices = self.get_invoices()
        # Ordering

        ordering = None
        if "ordering" in self.request.GET and self.request.GET["ordering"] in [
            "title",
            "-created_at",
            "file_size",
        ]:
            ordering = self.request.GET["ordering"]
        else:
            ordering = "title"

        documents = documents.order_by(ordering)
        # Search
        query_string = None
        if "q" in self.request.GET:
            form = SearchForm(self.request.GET, placeholder="Search documents")
            if form.is_valid():
                query_string = form.cleaned_data["q"]
                documents = documents.search(query_string)

        return documents

    def get(self, request, *args, **kwargs):
        collections = permission_policy.collections_user_has_any_permission_for(
            request.user, ["add", "change"]
        )
        if len(collections) < 2:
            collections = None
        else:
            collections = Collection.order_for_display(collections)

        # Create response
        return super().get(request, *args, **kwargs)

    def verife_http_response(self, request):
        if not request.is_ajax():
            return HttpResponseBadRequest("Cannot POST to this view without AJAX")

        if not request.FILES:
            return HttpResponseBadRequest("Must upload a file")
        return None

    def get_doc_form(self, request):
        # Build a form for validation
        DocumentForm = get_document_form(self.model)
        return DocumentForm(
            {
                "title": request.FILES["file"].name,
                "collection": request.POST.get("collection"),
            },
            {"file": request.FILES["file"]},
            user=request.user,
        )

    def save_doc(self, request, doc, doc_type):
        doc.doc_type = doc_type
        doc.uploaded_by_user = request.user
        doc.file_size = doc.file.size

        # Set new document file hash
        doc.file.seek(0)
        doc._set_file_hash(doc.file.read())
        doc.file.seek(0)
        doc.save()

    @vary_on_headers("X-Requested-With")
    def post(self, request, *args, **kwargs):

        respone = self.verife_http_response(request)
        if respone:
            return respone

        form = self.get_doc_form(request)

        if form.is_valid():
            # Save it
            doc = form.save(commit=False)

            doc_type = DocumentSushi.T_PERSONAL_INVOICES \
                if request.POST.get("type") == "invoice" else DocumentSushi.T_PERSONAL

            self.save_doc(request, doc, doc_type)

            shop = Shop.objects.get(id=self.kwargs["shop_id"])

            if request.POST.get("type") == "doc":
                shop.docs.add(doc)
                handle_materials(doc)
            elif request.POST.get("type") == "invoice":
                shop.checks.add(doc)
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


class ShopSignDetailView(UserPassesTestMixin, ListView):
    template_name = 'sushi_app/shopsign_detail.html'

    def get_queryset(self):
        shops = Shop.objects.filter(signs__id=self.kwargs['pk'])
        return shops

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign'] = ShopSign.objects.get(pk=self.kwargs['pk'])
        return context

    def test_func(self):
        return self.request.user.is_staff or self.request.user.user_profile.is_manager or self.request.user.user_profile.is_head


class ShopSignEditView(UserPassesTestMixin, UpdateView):
    model = Shop
    form_class = ShopSignEditForm
    template_name = 'store_sign_edit.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.user_profile.is_manager or self.request.user.user_profile.is_head

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(reverse_lazy("shop", args=[self.object.id]))


# # Create your views here
def manager_check(user):
    return user.user_profile.is_manager


def partner_check(user):
    return user.user_profile.is_partner


def head_check(user):
    return user.user_profile.is_head


@login_required
def base(request):
    employees_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile", "department"
    ).filter(head=request.user.user_profile)
    news_all = NewsPage.objects.all().order_by(
        'first_published_at')
    if len(news_all) == 0 or len(news_all) <= 3:
        news = news_all
    else:
        news = news_all[len(news_all) - 3:]
    return render(request, "index.html", {"employee_list": employees_list, "news": news})


@login_required
def employee_list(request):
    employees_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile",
    ).filter(
        head=request.user.user_profile) \
        if request.user.user_profile.is_head \
        else UserProfile.objects.prefetch_related(
        "user", "wagtail_profile", "department"
    ).filter(is_manager=True)
    return render(request, "employees.html", {"employee_list": employees_list, "breadcrumb": [{"title": "Сотрудники"}]})


@login_required
def employee_info(request, user_id):
    user = get_object_or_404(User, id=user_id)
    all_signs = {}
    shop_sign = ShopSign.objects.all()
    if hasattr(user, 'user_profile') and hasattr(user.user_profile, 'shop_partner'):
        user_shops_signs_ids = set(user.user_profile.shop_partner.values_list('signs__id', flat=True))
        if None in user_shops_signs_ids:
            user_shops_signs_ids.remove(None)
    for sign in shop_sign:
        all_signs[sign.title] = {'title': sign.title, 'id': sign.id, 'icon': sign.icon}
        if sign.id in user_shops_signs_ids:
            all_signs[sign.title]['active'] = True
        else:
            all_signs[sign.title]['active'] = False
    all_signs_sorted = sorted(all_signs.values(), key=lambda x: x['active'], reverse=True)
    return render(request, "employee.html", {"employee": user, "shop_sign": all_signs_sorted})


class EmployeeSignShopsView(ListView):
    template_name = "sushi_app/shops_list_by_sign.html"

    def get_queryset(self):
        shops = Shop.objects.filter(partner__user_id=self.kwargs['user_id'], signs__id=self.kwargs['sign_id'])
        return shops

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sign'] = ShopSign.objects.get(pk=self.kwargs['sign_id'])
        context['employee'] = User.objects.get(pk=self.kwargs['user_id'])
        return context


@login_required
def notification_view(request):
    notifications = Chat_Message.objects.select_related("sender", "task", "requests", "feedback", "idea",
                                                        "question").filter(recipient=request.user).order_by(
        '-created_at')
    paginator = Paginator(notifications, 10)
    page = request.GET.get('page')
    try:
        notifications = paginator.page(page)
    except PageNotAnInteger:
        notifications = paginator.page(1)
    except EmptyPage:
        notifications = paginator.page(paginator.num_pages)
    is_paginated = paginator.num_pages > 1
    return render(request, "notifications.html",
                  {"notifications": notifications, "is_paginated": is_paginated, "breadcrumb": [
                      {"title": "Оповещения"},
                  ]})


def get_filtered_tasks(request):
    ''' Возвращает список задачи сотрудника
        Если присутсвует GET параметр 'filter_task', то
        применяется фильтрация
    '''
    if request.user.user_profile.is_manager:
        tasks = Task.objects.prefetch_related("responsible") \
            .filter(manager=request.user.user_profile)
    else:
        tasks = Task.objects.prefetch_related("responsible") \
            .filter(responsible=request.user)
    if "filter_task" in request.GET:
        return tasks.filter(status=request.GET['filter_task'])
    return tasks


def get_filtered_request(request):
    if request.user.user_profile.is_manager:
        request_list = Requests.objects.prefetch_related("responsible").filter(
            manager=request.user.user_profile
        )
    else:
        request_list = Requests.objects.prefetch_related("responsible") \
            .filter(responsible=request.user)
    if "filter_request" in request.GET:
        return request_list.filter(status=request.GET['filter_request'])
    return request_list.order_by("-date_create")


def get_filtered_feedback(request):
    if request.user.user_profile.is_manager:
        feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
            manager=request.user.user_profile
        )
    else:
        feedback_list = Feedback.objects.prefetch_related("responsible", "shop").filter(
            responsible=request.user.user_profile
        )
    if "filter_feedback" in request.GET:
        return feedback_list.filter(status=request.GET['filter_feedback'])
    return feedback_list.order_by("-date_create")


def get_filtered_idea(request):
    StatusFormSet = modelformset_factory(IdeaModel, form=IdeaStatusForm, extra=0)
    formset = StatusFormSet(request.POST or None, queryset=IdeaModel.objects.filter(recipient=request.user),
                            prefix='idea')
    if request.user.user_profile.is_manager:
        idea_list = IdeaModel.objects.select_related("sender", "recipient").filter(
            recipient=request.user
        )
    else:
        idea_list = IdeaModel.objects.select_related("sender", "recipient").filter(
            sender=request.user
        )
    if "filter_idea" in request.GET:
        return (idea_list.filter(status=request.GET['filter_idea']), StatusFormSet(request.POST or None,
                                                                                   queryset=IdeaModel.objects.filter(
                                                                                       recipient=request.user,
                                                                                       status=request.GET[
                                                                                           'filter_idea']),
                                                                                   prefix='idea'))
    return (idea_list, formset)


@login_required
@user_passes_test(manager_check)
def faq_list(request):
    faq_all = QuestionModel.objects.all()
    return render(request, "faq_list.html", {"faq_all": faq_all})


@login_required
@user_passes_test(manager_check)
def faq_answer(request, faq_id):
    question = get_object_or_404(QuestionModel, id=faq_id)
    old_answer = question.answer
    form = AnswerForm(request.POST or None, instance=question)
    if form.is_valid():
        new_q = form.save(commit=False)
        new_q.status = QuestionModel.ST_REJECTED if new_q.hide else QuestionModel.ST_OK
        new_q._old_answer = old_answer
        new_q.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=question.user,
            body=f"Дан ответ на вопрос {new_q.theme}",
            question=question
        )
        return HttpResponseRedirect(reverse_lazy("faq_list"))
    return render(
        request,
        "faq_answer.html",
        {
            "question": question,
            "form": form,
            "breadcrumb": [
                {"title": "Список вопросов", "url": reverse_lazy("faq_list")},
                {"title": "Добавить ответ"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def manager_lk_view(request):
    partner_list = UserProfile.objects.prefetch_related(
        "user", "wagtail_profile"
    ).filter(manager=request.user.user_profile)
    task_not_solved = Task.objects.filter(status=ST_IN_PROGRESS,
                                          manager=request.user.user_profile).count()
    requests_not_solved = Requests.objects.filter(status=ST_IN_PROGRESS,
                                                  manager=request.user.user_profile).count()
    ideas_not_solved = IdeaModel.objects.filter(status=IdeaModel.ST_CONSIDERATION,
                                                recipient=request.user).count()
    feedback_not_solved = Feedback.objects.filter(status=Feedback.ST_NOT_SOLVED,
                                                  manager=request.user.user_profile).count()
    request_list = get_filtered_request(request)
    task_list = get_filtered_tasks(request)
    feedback_list = get_filtered_feedback(request)
    page_object = Paginator(DocumentSushi.objects.all(), 9)
    is_paginated = False
    page = request.GET['page'] if 'page' in request.GET else 1
    page_obj = documents = page_object.get_page(page)
    data = get_filtered_idea(request)
    idea_list = data[0]
    formset = data[1]
    if formset.is_valid():
        formset.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER') + "#ideas")
    return render(
        request,
        "dashboard_manager.html",
        {
            'idea_list': idea_list,
            'formset': formset,
            "partner_list": partner_list,
            "request_list": request_list,
            "task_list": task_list,
            "task_not_solved": task_not_solved,
            "ideas_not_solved": ideas_not_solved,
            "requests_not_solved": requests_not_solved,
            "feedback_not_solved": feedback_not_solved,
            "feedback_list": feedback_list,
            "breadcrumb": [{"title": "Личный кабинет"}],
            "documents": documents,
            "page_obj": page_obj,
            "is_paginated": is_paginated

        },
    )


@csrf_exempt
def load_filtered_idea(request):
    data = get_filtered_idea(request)
    idea_list = data[0]
    formset = data[1]
    return render(
        request,
        'partials/ideas_manager.html',
        {'idea_list': idea_list, 'formset': formset}
    )


@csrf_exempt
def load_filtered_tasks(request):
    task_list = get_filtered_tasks(request)
    return render(
        request,
        'partials/tasks_manager.html',
        {'task_list': task_list}
    )


@csrf_exempt
def load_filtered_request(request):
    request_list = get_filtered_request(request)
    return render(
        request,
        'partials/request_manager.html',
        {'request_list': request_list}
    )


@csrf_exempt
def load_filtered_feedback(request):
    feedback_list = get_filtered_feedback(request)
    return render(
        request,
        'partials/feedback_manager.html',
        {'feedback_list': feedback_list}
    )


def _get_params_if_exists(request, *args, **kwargs):
    ''' args ключи, kwargs ключи со значением по дефолту '''

    params = {}
    for arg in args:
        if arg not in kwargs:
            kwargs[arg] = None

    for k, default in kwargs.items():

        added = False
        if default:
            params[k] = request.GET.get(k, default)
            added = True
        elif k in request.GET:
            params[k] = request.GET[k]
            added = True

        if added and isinstance(params[k], str) and params[k].isdigit():
            params[k] = int(params[k])

    return params


def _load_docs(request, current_page=1, doc_type=None, sub_type=None):
    count_objects = 9
    offset = (current_page * count_objects) - count_objects
    limmit = (current_page * count_objects)
    print(offset, limmit)
    if doc_type:
        docs = DocumentSushi.objects.filter(doc_type=doc_type)[offset: limmit]
    else:
        docs = []

    if sub_type:
        docs = DocumentSushi.objects.filter(sub_type=sub_type)[offset: limmit]

    return docs


@csrf_exempt
def load_docs(request):
    args = ['doc_type', 'sub_type']
    params = _get_params_if_exists(request, *args, current_page=1)
    docs = _load_docs(request, **params)
    context = {
        'documents': docs,
        'refresh_token': secrets.token_hex(16)
    }
    return render(request, 'partials/documents.html', context)


@csrf_exempt
def load_docs_info(request):
    ''' принимиет json со спискос id документов '''

    ids = [int(i) for i in json.loads(request.body)]
    docs = DocumentSushi.objects.filter(pk__in=ids)
    urls = {doc.id: doc.url for doc in docs}

    # сопоставляем каждому документу ссылку на выделенное превью в случае её наличия
    preview_docs = DocumentPreview.objects.filter(base_document_id__in=(doc.id for doc in docs))
    for pdoc in preview_docs:
        urls[pdoc.base_document.id] = pdoc.preview_file.url

    id_to_preview_type = dict()
    for doc in docs:
        ext = doc.file_extension.lower()
        if ext in CONVERT_TO_PDF_EXTENSIONS:
            id_to_preview_type[doc.id] = 'embed'

        if ext == 'pdf':
            id_to_preview_type[doc.id] = 'clear_pdf'

        if ext in ('xls', 'xlsx'):
            id_to_preview_type[doc.id] = 'excel'

        if ext in IMAGE_TYPES:
            id_to_preview_type[doc.id] = 'image'

    res = {
        'docs_id_to_url': urls,
        'id_to_preview_type': id_to_preview_type
    }

    return JsonResponse(res)


@csrf_exempt
def load_pdf_stream_preview(request, doc_id):
    with DocumentSushi.objects.get(pk=doc_id).file.open('rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=some_file.pdf'
        return response


@csrf_exempt
def load_excel(request, doc_id):
    with DocumentSushi.objects.get(pk=doc_id).file.open('rb') as f:
        excel_df = pd.read_excel(f);
        response = HttpResponse(excel_df.to_html())
        return response


@csrf_exempt
def preview_deprecated(request, doc_type, doc_id):
    doc = DocumentSushi.objects.filter(pk=doc_id).first()
    doc_url = doc.url
    preview_doc = DocumentPreview.objects.filter(base_document_id=doc_id).first()
    if preview_doc:
        doc_url = preview_doc.preview_file.url

    context = {
        'doc_type': doc_type,
        'doc_id': doc_id,
        'doc_url': doc_url
    }
    return render(request, 'file_preview_deprecated.html', context)


@csrf_exempt
def preview(request, doc_type, doc_id):
    doc = DocumentSushi.objects.filter(pk=doc_id).first()
    doc_url = doc.url
    preview_doc = DocumentPreview.objects.filter(base_document_id=doc_id).first()
    if preview_doc:
        doc_url = preview_doc.preview_file.url

    context = {
        'doc_type': doc_type,
        'doc_id': doc_id,
        'doc_url': doc_url
    }
    return render(request, 'file_preview.html', context)


@csrf_exempt
def load_paginations_docs(request):
    current_page = int(request.GET.get('page', 1))
    if 'doc_type' in request.GET:
        docs = DocumentSushi.objects.filter(doc_type=request.GET['doc_type'])
    else:
        docs = []

    if docs and 'sub_type' in request.GET:
        docs = docs.filter(sub_type=request.GET['sub_type'])

    page_object = Paginator(docs, 9)
    return render(
        request,
        'partials/pagination.html',
        {'posts': page_object.get_page(current_page)}
    )


@login_required
@user_passes_test(partner_check)
def partner_lk_view(request):
    shop_list = Shop.objects.prefetch_related("checks", "docs").filter(
        partner=request.user.user_profile
    )
    task_not_solved = Task.objects.filter(status=ST_IN_PROGRESS,
                                          responsible=request.user).count()
    feedback_not_solved = Feedback.objects.filter(status=Feedback.ST_NOT_SOLVED,
                                                  responsible=request.user.user_profile).count()
    requests_not_solved = Requests.objects.filter(status=ST_IN_PROGRESS,
                                                  responsible=request.user).count()
    request_list = get_filtered_request(request)
    task_list = get_filtered_tasks(request)
    feedback_list = get_filtered_feedback(request)
    documents = DocumentSushi.objects.all()
    page_object = Paginator(documents, 9)
    is_paginated = False
    page_obj = documents = []
    if page_object.num_pages > 0:
        is_paginated = True
        page = request.GET['page'] if 'page' in request.GET else 1
        page_obj = documents = page_object.get_page(page)

    return render(
        request,
        "dashboard_partner.html",
        {
            "shop_list": shop_list,
            "request_list": request_list,
            "task_list": task_list,
            "feedback_not_solved": feedback_not_solved,
            "task_not_solved": task_not_solved,
            "requests_not_solved": requests_not_solved,
            "feedback_list": feedback_list,
            "breadcrumb": [{"title": "Личный кабинет"}],
            "manager": request.user.user_profile.manager,
            "documents": documents,
            "page_obj": page_obj,
            "is_paginated": is_paginated
        },
    )


@login_required
@user_passes_test(partner_check)
def form_request_view(request):
    form = RequestsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        req = form.save(commit=False)
        req.responsible = request.user
        req.manager = request.user.user_profile.manager
        req.save()
        if 'file' in request.FILES:
            for f in request.FILES.getlist('file'):
                RequestFile.objects.create(file=f, request=req)
        Chat_Message.objects.create(
            sender=request.user,
            recipient=request.user.user_profile.manager.user,
            body="Создан запрос",
            requests=req
        )
        return HttpResponseRedirect(reverse_lazy("partner_lk"))
    return render(
        request,
        "request_new.html",
        {
            "manager": request.user.user_profile.manager,
            "form": form,
            "breadcrumb": [
                {"title": "Личный кабинет", "url": reverse_lazy("partner_lk")},
                {"title": "Добавить задачу"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def form_task_view(request, partner_id):
    partner = get_object_or_404(UserProfile, id=partner_id)
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = partner.user
        form.manager = request.user.user_profile
        form.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=partner.user,
            body=f"Создана задача от {request.user.get_full_name()}",
            task=form
        )
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    return render(
        request,
        "task_new.html",
        {
            "partner": partner,
            "form": form,
            "breadcrumb": [
                {
                    "title": partner.user.get_full_name,
                    "url": reverse("employee_info", args=[partner.user.id]),
                },
                {"title": "Добавить задачу"},
            ],
        },
    )


@login_required
@user_passes_test(manager_check)
def feedback_form_view(request):
    form = FeedbackForm(request.POST or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.responsible = form.shop.partner
        form.manager = request.user.user_profile
        form.save()
        Chat_Message.objects.create(
            sender=request.user,
            recipient=form.shop.partner.user,
            body=f"Создан отзыв на магазин {form.shop}",
            feedback=form
        )
        return HttpResponseRedirect(reverse_lazy("manager_lk"))
    context = {
        "form": form,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить отзыв"},
        ],
    }
    return render(request, "review_new.html", context)


@login_required
@user_passes_test(manager_check)
def create_partner_view(request):
    form_user = RegistrationEmployeeMainForm(
        request.POST or None, request.FILES or None, prefix="user"
    )
    form_user_profile = RegistrationPartnerAdditionForm(
        request.POST or None, request.FILES or None, prefix="user_profile"
    )
    if form_user.is_valid() and form_user_profile.is_valid():
        form_user = form_user.save(commit=False)
        form_user.set_password(form_user.password)
        form_user.save()
        editor_group = Group.objects.get(name='Editors')
        form_user.groups.add(editor_group)
        wagtail_user = wagtail.users.models.UserProfile.get_for_user(form_user)
        wagtail_user.avatar = form_user_profile.cleaned_data["avatar"]
        wagtail_user.preferred_language = settings.LANGUAGE_CODE
        wagtail_user.current_time_zone = settings.TIME_ZONE
        wagtail_user.save()
        form_user_profile = form_user_profile.save(commit=False)
        form_user_profile.user = form_user
        form_user_profile.wagtail_profile = wagtail_user
        form_user_profile.manager = request.user.user_profile
        form_user_profile.is_partner = True
        form_user_profile.save()
        return HttpResponseRedirect(reverse("employee_info", args=[form_user.id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить франчайзи"},
        ],
    }
    return render(request, "user_new.html", context)


@login_required
@user_passes_test(manager_check)
def edit_partner_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form_user = EditEmployeeMainForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user),
        instance=user,
        prefix="user",
    )
    form_user_profile = EditPartnerAdditionForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.user_profile),
        instance=user.user_profile,
        prefix="user_profile",
    )
    form_wagtail = AvatarPreferencesForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.wagtail_userprofile),
        instance=user.wagtail_userprofile,
        prefix="user_profile",
    )
    if (
            form_user.is_valid()
            and form_user_profile.is_valid()
            and form_wagtail.is_valid()
    ):
        form_user.save()
        form_user_profile.save()
        form_wagtail.save()
        return HttpResponseRedirect(reverse("employee_info", args=[user_id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "form_wagtail": form_wagtail,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Редактировать франчайзи"},
        ],
    }
    return render(request, "user_edit.html", context)


@login_required
@user_passes_test(head_check)
def create_employee_view(request):
    form_user = RegistrationEmployeeMainForm(
        request.POST or None, request.FILES or None, prefix="user"
    )
    form_user_profile = RegistrationEmployeeAdditionForm(
        request.POST or None, request.FILES or None, prefix="user_profile"
    )
    if form_user.is_valid() and form_user_profile.is_valid():
        form_user = form_user.save(commit=False)
        form_user.set_password(form_user.password)
        form_user.save()
        editor_group = Group.objects.get(name='Editors')
        form_user.groups.add(editor_group)
        wagtail_user = wagtail.users.models.UserProfile.get_for_user(form_user)
        wagtail_user.avatar = form_user_profile.cleaned_data["avatar"]
        wagtail_user.preferred_language = settings.LANGUAGE_CODE
        wagtail_user.current_time_zone = settings.TIME_ZONE
        wagtail_user.save()
        form_user_profile = form_user_profile.save(commit=False)
        form_user_profile.user = form_user
        form_user_profile.wagtail_profile = wagtail_user
        form_user_profile.head = request.user.user_profile
        form_user_profile.is_manager = True
        form_user_profile.save()
        return HttpResponseRedirect(reverse("employee_info", args=[form_user.id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить сотрудника"},
        ],
    }
    return render(request, "employee_new.html", context)


@login_required
def edit_employee_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user != request.user:
        if request.user.user_profile.is_partner:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_user = EditEmployeeMainForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user),
        instance=user,
        prefix="user",
    )
    form_user_profile = EditEmployeeAdditionForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.user_profile),
        instance=user.user_profile,
        prefix="user_profile",
    )
    form_wagtail = AvatarPreferencesForm(
        request.POST or None,
        request.FILES or None,
        initial=model_to_dict(user.wagtail_userprofile),
        instance=user.wagtail_userprofile,
        prefix="user_profile",
    )
    if (
            form_user.is_valid()
            and form_user_profile.is_valid()
            and form_wagtail.is_valid()
    ):
        form_user.save()
        form_user_profile.save()
        form_wagtail.save()
        return HttpResponseRedirect(reverse("employee_info", args=[user_id]))
    context = {
        "form_user": form_user,
        "form_user_profile": form_user_profile,
        "form_wagtail": form_wagtail,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Редактировать сотрудника"},
        ],
    }
    return render(request, "employee_edit.html", context)


@login_required
@user_passes_test(manager_check)
def shop_form_view(request):
    form = ShopForm(request.POST or None)
    if form.is_valid():
        shop = form.save()
        sign = ShopSign.objects.filter(pk__in=request.POST.getlist('signs'))
        shop.signs.add(*sign)
        return HttpResponseRedirect(reverse_lazy("shop", args=[shop.id]))
    context = {
        "form": form,
        "breadcrumb": [
            {"title": "Личный кабинет", "url": reverse_lazy("manager_lk")},
            {"title": "Добавить магазин"},
        ],
    }
    return render(request, "store_new.html", context)


# @login_required
# def shop_view(request, shop_id):
#     shop = get_object_or_404(Shop, id=shop_id)
#     return render(request, 'store.html', {'shop': shop,
#                                           'breadcrumb': [{'title': 'Личный кабинет',
#                                                           'url': reverse_lazy('partner_lk')},
#                                                          {'title': f"Магазин #{shop.id}"}]})


@login_required
def task_view(request, task_id, user_id):
    task = get_object_or_404(Task, id=task_id)
    if task.responsible != request.user:
        if task.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusTaskForm(
        request.POST or None, initial=model_to_dict(task), instance=task
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            new_status = form_status.save(commit=False)
            if new_status.status == ST_SOLVED:
                Chat_Message.objects.create(
                    sender=request.user,
                    recipient=task.responsible,
                    body="Задача переведена в статус решена",
                    task=new_status
                )
            new_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        task=task, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        task=task, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        task_new = form.save(commit=False)
        task_new.task = task
        task_new.from_user = request.user
        if request.user == task.responsible:
            task_new.to_user = task.manager.user
        else:
            task_new.to_user = task.responsible
        task_new.save()
        Chat_Message.objects.create(
            sender=task_new.from_user,
            recipient=task_new.to_user,
            body=task_new.text,
            task=task
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#coments")
    return render(
        request,
        "task.html",
        {
            "task": task,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Задача #{task.id}"},
            ],
        },
    )


@login_required
def requests_view(request, requests_id, user_id):
    requests = get_object_or_404(Requests, id=requests_id)
    if requests.responsible != request.user:
        if requests.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusRequestsForm(
        request.POST or None, initial=model_to_dict(requests), instance=requests
    )
    if request.user.user_profile.is_manager:
        if form_status.is_valid():
            form_status.save()
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        requests=requests, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        requests=requests, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.requests = requests
        form.from_user = request.user
        if request.user == requests.responsible:
            form.to_user = requests.manager.user
        else:
            form.to_user = requests.responsible
        form.save()
        Chat_Message.objects.create(
            sender=form.from_user,
            recipient=form.to_user,
            body=form.text,
            requests=requests
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#coments")
    return render(
        request,
        "request.html",
        {
            "requests": requests,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Запрос #{requests.id}"},
            ],
        },
    )


@login_required
def feedback_view(request, feedback_id, user_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback._request_user = request.user
    if feedback.responsible != request.user.user_profile:
        if feedback.manager != request.user.user_profile:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    form_status = StatusFeedbackForm(
        request.POST or None, initial=model_to_dict(feedback), instance=feedback
    )
    if form_status.is_valid():
        form_status.save()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    qs1 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        feedback=feedback, from_user=request.user.id
    )
    qs2 = Messeges.objects.prefetch_related("from_user", "to_user").filter(
        feedback=feedback, to_user=request.user.id
    )
    messeges = qs1.union(qs2).order_by("date_create")
    form = MessegesFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form = form.save(commit=False)
        form.feedback = feedback
        form.from_user = request.user
        if request.user == feedback.responsible.user:
            form.to_user = feedback.manager.user
        else:
            form.to_user = feedback.responsible.user
        form.save()
        Chat_Message.objects.create(
            sender=form.from_user,
            recipient=form.to_user,
            body=form.text,
            feedback=feedback
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER") + "#coments")
    return render(
        request,
        "review.html",
        {
            "feedback": feedback,
            "messeges": messeges,
            "form": form,
            "form_status": form_status,
            "breadcrumb": [
                {
                    "title": "Личный кабинет",
                    "url": reverse_lazy("partner_lk")
                    if request.user.user_profile.is_partner
                    else reverse_lazy("manager_lk"),
                },
                {"title": f"Отзыв #{feedback.id}"},
            ],
        },
    )


@login_required
def notification_settings_view(request):
    def _build_input_info(dict_, name_prefix, sort_map):
        return [{
            'name': f'{name_prefix}_{key}',
            'val': key,
            'checked': 'checked' if dict_[key] else ''
        } for key in sorted(dict_.keys(),
                            key=lambda x: sort_map[x])]

    context = {
        "breadcrumb": [
            {
                "title": "Личный кабинет",
                "url": reverse_lazy("partner_lk")
                if request.user.user_profile.is_partner
                else reverse_lazy("manager_lk"),
            },
            {"title": "Настройки уведомлений"},
        ],
    }

    is_manager = request.user.user_profile.is_manager
    exclude_choices = []
    if is_manager:
        exclude_choices = [TASK_T]

    user_available_choices = list(filter(lambda x: x[0] not in exclude_choices,
                                         EVENT_TYPE_CHOICES))
    if not is_manager:
        request_key = list(filter(lambda a: a[0] == REQUEST_T,
                                  user_available_choices))[0]
        index = user_available_choices.index(request_key)
        user_available_choices[index] = (REQUEST_T, 'Задачи менеджеру')

    event_types = [j[0] for j in user_available_choices]

    site_rules = {i: False for i in event_types}
    email_rules = {i: False for i in event_types}
    site_rule_name = SUBSCRIBE_TYPE_CHOICES[0][0]
    email_rule_name = SUBSCRIBE_TYPE_CHOICES[1][0]

    for event in Subscribes.objects.filter(user_id=request.user.id):
        if event.subscribe_type == email_rule_name:
            email_rules[event.event_type] = True

        if event.subscribe_type == site_rule_name:
            site_rules[event.event_type] = True

    sort_map = {j: i for i, j in enumerate(event_types)}

    context['names'] = [i[1] for i in sorted(user_available_choices, key=lambda x: sort_map[x[0]])]
    context['site_rules'] = _build_input_info(site_rules, site_rule_name, sort_map)
    context['email_rules'] = _build_input_info(email_rules, email_rule_name, sort_map)

    return render(request, 'notification_settings.html', context)


@csrf_exempt
@login_required
def update_notification_rules(request):
    subs = Subscribes.objects.filter(user_id=request.user.id)
    subs_d = {(x.event_type, x.subscribe_type): x for x in subs}
    models = []
    for k, v in request.POST.items():
        prefix, event_type = k.split('_')

        key = (prefix, event_type)

        if key in subs_d:
            del subs_d[key]
            continue

        sub = Subscribes(user_id=request.user,
                         event_type=event_type,
                         subscribe_type=prefix)

        models.append(sub)

    Subscribes.objects.bulk_create(models)
    for _, v in subs_d.items():
        v.delete()

    return HttpResponseRedirect(reverse_lazy('notification'))


@login_required
def load_notifcations(request):
    subs = Subscribes.objects.filter(subscribe_type=REALTIME_C,
                                     user_id=request.user.id)

    res = {}

    for sub in subs.all():
        for event in sub.subscribe_events.order_by('date_of_creation').all():
            res[event.pk] = {
                'type': event.event_type,
                'status': event.value,
                'entityId': event.event_id
            }

    return JsonResponse(res)


@login_required
@csrf_exempt
def notifcation_events(request):
    if request.is_ajax():
        if request.method == 'POST':
            events = [int(i) for i in json.loads(request.body)]
            NotificationEvents.objects.filter(pk__in=events).delete()

    return JsonResponse({})
