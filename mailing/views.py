from base64 import b64decode
import json

from django.core.files.base import ContentFile
from django.shortcuts import render, Http404, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django import forms
from django.views.generic import View, ListView, TemplateView
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


from .models import UserProfile, Mailing


def error_gen(meta: dict, link: str) -> str:
    return json.dumps({
        "meta": meta,
        "link": link
    })


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['title', 'content', 'senders', 'to_create']
        error_messages = {
            'senders': {
                'required': 'Выберете значения поля для поля получатель '
            },
            'title': {
                'max_length': "Достигнуто максимальное количкство символов для заголовка.",
                'required': 'Заголовок не может быть пустым'

            },
            'content': {
                'max_length': "Достигнуто максимальное количество символов для текста рассылки.",
                'required': 'Текст рассылки не может быть пустым'
            },

        }


class SingleView(LoginRequiredMixin, TemplateView):
    http_method_names = ['get', ]
    template_name = "mailing/single_view.html"

    def get_context_data(self, **kwargs):
        kwargs['obj'] = get_object_or_404(Mailing, pk=kwargs['pk'])
        return kwargs


class MessageNewView(LoginRequiredMixin, View):
    http_method_names = ['get', 'post']

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def work_flow(self, data: list) -> (dict, list):
        obj = {
        }
        files = []
        for i in data:
            name = i['name']
            value = i['value']
            try:
                if name == "files[]":
                    meta, img_str = value.split(';base64,')
                    # if i.get('filename'):
                    #     name = i.get('filename')
                    # else:
                    #     name = '{}.{}'.format(int(time.time() * 1000), meta.split('/')[-1])
                    # If use white list ext
                    # if meta.split('/')[-1] in ['png','jpeg']:
                    #     data = ContentFile(b64decode(img_str))
                    #     files.append(
                    #         data
                    #     )
                    name = i.get('filename')
                    files.append({"name": name,
                                  "content": ContentFile(b64decode(img_str))})

                else:
                    obj[name].append(value)
            except KeyError:
                obj[name] = []
                obj[name].append(value)
        return obj, files

    def save_data(self, data_dict: dict) -> Mailing:
        instance = {}
        try:
            if len("".join(data_dict.get('title'))):
                instance['title'] = "".join(data_dict.get('title'))
            if "<p><br></p>" != "".join(data_dict.get('content')):
                instance['content'] = "".join(data_dict.get('content'))
            if data_dict.get('partners2[]'):
                instance['senders'] = data_dict.get('partners2[]')
            else:
                instance['senders'] = data_dict.get('partners1[]')
        except KeyError:
            pass
        instance['to_create'] = self.request.user.pk
        form = MailingForm(instance)
        if form.is_valid():
            # import pdb;pdb.set_trace()
            obj = form.save()
            return obj
        else:
            raise Exception(form.errors)

    @transaction.atomic
    def create_new(self, data: list) -> str:
        obj = self.save_data(data[0])
        obj.save_files(data[1])
        # send for emails
        for user_profile in obj.senders.all():
            if isinstance(user_profile.user.email, str):
                self.send_massage(obj, user_profile.user.email)
        return obj

    def send_massage(self, obj, to_email):
        try:

            template = 'emails/mailing_news.html'
            message = render_to_string(template, obj)
            error = send_mail("Появилась новая рассылка", message, settings.SERVER_EMAIL, [to_email, ])
            if not error:
                raise Exception('Ошибка отправления письма')
        except Exception as _:
            raise Exception('Ошибка отправления письма')

    def post(self, *args, **kwargs):
        try:
            # convert string to json
            data = json.loads(self.request.body)
            # data grouping
            data_groups = self.work_flow(data['data'])
            # # create new mailing
            new_mailing = self.create_new(data_groups)

            obj = error_gen(
                meta={
                    "error": 201,
                    "messages": ['Create news is successful', ]
                },
                link=new_mailing.url()
            )

            return HttpResponse(obj, content_type="application/json")

        except Exception as e:
            """ return error for view in frontend """
            return HttpResponse(
                error_gen({
                    "error": 400,
                    "messages": [str(e)]
                },
                    link=''
                ),
                content_type="application/json"
            )

    def get(self, *args, **kwargs):
        user_profile = self.request.user.user_profile

        if user_profile.is_head:
            partner_list = UserProfile.objects.prefetch_related(
                "user", "wagtail_profile"
            ).filter(is_partner=True)
        elif user_profile.is_manager:
            partner_list = UserProfile.objects.prefetch_related(
                "user", "wagtail_profile"
            ).filter(manager=self.request.user.user_profile)
        else:
            partner_list = []
        return render(self.request, "mailing/create_form.html", {"partners": partner_list, })


class MailListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/list_view.html'
    paginate_by = 9

    def get_queryset(self):
        user_profile = self.request.user.user_profile
        if user_profile.is_manager:
            return self.model.objects.filter(to_create=self.request.user)
        elif user_profile.is_partner:
            return self.model.objects.filter(senders__in=[user_profile, ])
        else:
            raise Http404()
