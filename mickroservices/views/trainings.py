from django.views.generic import ListView
from django.views.generic.detail import DetailView

from mickroservices.models import CourseModel


class CoursesView(ListView):
    template_name = 'lessons.html'
    model = CourseModel
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(CoursesView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [{'title': 'Обучение'}]
        return context


class CourseView(DetailView):
    template_name = 'schedule.html'
    model = CourseModel
