from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.urls import reverse_lazy

from mickroservices.models import CourseModel, ScheduleModel
from mickroservices.forms import ScheduleForm


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


class ScheduleListView(ListView):
    template_name = 'schedule.html'
    model = ScheduleModel
    paginate_by = 10
    context_object_name = 'schedule_list'

    def get_context_data(self, **kwargs):
        context = super(ScheduleListView, self).get_context_data(**kwargs)
        context['breadcrumb'] = [
            {'title': 'Обучение',
             'url': reverse_lazy('mickroservices:lessons')},
            {'title': 'Расписание'}
        ]
        return context


class ScheduleView(UpdateView):
    template_name = 'schedule_form.html'
    form_class = ScheduleForm
    model = ScheduleModel
    success_url = reverse_lazy('mickroservices:schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleView, self).get_context_data(**kwargs)
        context['title'] = 'Редактировать расписание'
        context['breadcrumb'] = [
            {'title': 'Обучение',
             'url': reverse_lazy('mickroservices:lessons')},
            {'title': 'Расписание',
             'url': reverse_lazy('mickroservices:schedule')},
            {'title': context['title']}
        ]
        return context

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        return TemplateResponse(self.request, self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})


class ScheduleCreateView(CreateView):
    template_name = 'schedule_form.html'
    form_class = ScheduleForm
    success_url = reverse_lazy('mickroservices:schedule')

    def get_context_data(self, **kwargs):
        context = super(ScheduleCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Добавить расписание'
        context['breadcrumb'] = [
            {'title': 'Обучение',
             'url': reverse_lazy('mickroservices:lessons')},
            {'title': 'Расписание',
             'url': reverse_lazy('mickroservices:schedule')},
            {'title': context['title']}
        ]
        return context

    def form_invalid(self, form, ms='Ошибка заполнения формы'):
        print(form.errors)
        print(form.cleaned_data)
        return TemplateResponse(self.request, self.template_name,
                                {'form': form,
                                 'status_ms': True,
                                 'message': ms})
