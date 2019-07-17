from django.views.generic import ListView

from mickroservices.models import MarketingMaterial


class MarketingView(ListView):
    template_name = 'marketingmaterial.html'
    model = MarketingMaterial
    paginate_by = 9
    context_object_name = 'materials'

    def get_context_data(self, **kwargs):
        context = super(MarketingView, self).get_context_data(**kwargs)

        context['types_marketing'] =\
            (item[1] for item in MarketingMaterial.TYPE_CHOICE)
        context['breadcrumb'] = [{'title': 'Маркетинговые материалы'}]

        return context
