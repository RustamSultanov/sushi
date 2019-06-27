from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# Now register the new UserAdmin# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.register(Product)
admin.site.register(Messeges)
admin.site.register(Feedback)

