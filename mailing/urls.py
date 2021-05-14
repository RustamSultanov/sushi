from django.urls import path

from .func_view import download_mail_files
from  .views import MessageNewView, MailListView, SingleView


app_name = 'mailing'

urlpatterns = [
    path('create/', MessageNewView.as_view(), name= 'mailing_create'),
    path('single_view/<int:pk>/', SingleView.as_view(), name="mailing_view"),
    path('list_view/', MailListView.as_view(), name="mailing_view_list"),
    path('download/', download_mail_files, name="download_mail_files"),
]
