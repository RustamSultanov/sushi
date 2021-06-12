from django.urls import path

from . import views

urlpatterns = [
    path(
        'close_message_chat/', views.close_message, name='close_message'),
    path('chat_page/', views.ChatPage.as_view(), name='chat_page'),
    path('new_group', views.new_group, name='new_chat_group'),
]
