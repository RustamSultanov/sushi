from django.views.generic import ListView

from mickroservices.models import NewsPage


class NewsView(ListView):
    template_name = 'news.html'
    model = NewsPage
    paginate_by = 9
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(NewsView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title':'Новости'}]
        return context
