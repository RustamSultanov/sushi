from django.contrib import admin
from .models import ChatMessage, Room
# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(Room)
