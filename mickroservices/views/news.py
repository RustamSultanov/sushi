from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from wagtail.core.models import Page

from mickroservices.forms import NewsForm
from mickroservices.models import NewsPage


class NewsView(ListView):
    template_name = 'news.html'
    model = NewsPage
    paginate_by = 9
    context_object_name = 'news'
    ordering = 'first_published_at'

    def get_queryset(self):
        news_all = self.model.objects.filter(
            live=True,
            go_live_at__lt=timezone.now()
        ).order_by('first_published_at')
        return news_all

    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Новости'}]
        return context


class NewsCreateView(CreateView):
    template_name = 'news_form.html'
    form_class = NewsForm
    success_url = reverse_lazy('mickroservices:news')

    def dispatch(self, request, *args, **kwargs):
        if not (self.request.user.user_profile.is_manager or self.request.user.user_profile.is_head):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewsCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Создание новости'
        context['breadcrumb'] = [
            {'title': 'Новости',
             'url': reverse_lazy('mickroservices:news')},
            {'title': context['title']}
        ]
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title, allow_unicode=True)
        self.object.seo_title = self.object.title
        homepage = Page.objects.get(url_path='/home/')
        homepage.add_child(instance=self.object)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request,
                                self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})


class NewsEditView(UpdateView):
    template_name = 'news_form.html'
    form_class = NewsForm
    model = NewsPage
    success_url = reverse_lazy('mickroservices:news')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user_profile.user_is_manager:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(NewsEditView, self).get_context_data(**kwargs)
        context['title'] = 'Редактирование новости'
        context['breadcrumb'] = [
            {'title': 'Новости',
             'url': reverse_lazy('mickroservices:news')},
            {'title': context['title']}
        ]
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.slug = slugify(self.object.title, allow_unicode=True)
        self.object.seo_title = self.object.title
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request,
                                self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})


class NewsDeleteView(DeleteView):
    model = NewsPage
    template_name = 'delete_news.html'
    success_url = reverse_lazy('mickroservices:news')

    def get_success_url(self):
        return self.success_url

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.user_profile.user_is_manager:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            url = self.get_success_url()
            return HttpResponseRedirect(url)
        else:
            return super(NewsDeleteView, self).post(request, *args, **kwargs)
