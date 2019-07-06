from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from mickroservices.models import CourseModel



class CoursesView(ListView):
    template_name ='lessons.html'
    model = CourseModel
    paginate_by = 10


class CourseView(DetailView):
    template_name ='schedule.html'
    model = CourseModel
