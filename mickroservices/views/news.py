from django.template.response import TemplateResponse
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.utils.text import slugify

from mickroservices.models import NewsPage
from mickroservices.forms import NewsForm
from wagtail.core.models import Page


class NewsView(ListView):
    template_name = 'news.html'
    model = NewsPage
    paginate_by = 9
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Новости'}]
        return context


class NewsCreateView(FormView):
    template_name = 'news_form.html'
    form_class = NewsForm
    success_url = reverse_lazy('mickroservices:news')

    def post(self, request, *args, **kwargs):
        
        form = NewsForm(request.POST)
        if form.is_valid():
            self.form_valid(form)



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
        print('================')
        print(form.cleaned_data)
        homepage = Page.objects.get(url_path='/home/')
        page = NewsPage(
            title=form.cleaned_data['title'],
            slug=slugify(form.cleaned_data['title']),
            content=form.cleaned_data['body'],
            body=form.cleaned_data['body'])
        homepage.add_child(instance=page)

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request,
                                self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})
