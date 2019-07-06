from django.urls import path

from .views import QuestionView

app_name = 'mickroservices'

urlpatterns = [
    path('faq/', QuestionView.as_view(), name='faq'),
]