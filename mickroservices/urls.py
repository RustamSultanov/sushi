from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import QuestionView, CoursesView, CourseView

app_name = 'mickroservices'

urlpatterns = [
    path('faq/', login_required(QuestionView.as_view()), name='faq'),
    path('lessons/', login_required(CoursesView.as_view()), name='lessons'),
    path('lesson/<int:pk>', login_required(CourseView.as_view()), name='lesson'),
]