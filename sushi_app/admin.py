from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
import wagtail.users.models
from django.template.defaultfilters import truncatewords
from feincms.admin import tree_editor

# Now register the new UserAdmin# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Users'


class WagtailUserProfileInline(admin.StackedInline):
    model = wagtail.users.models.UserProfile
    can_delete = False
    verbose_name_plural = 'WagtailUsers'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, WagtailUserProfileInline)

@admin.register(Messeges)
class MessegesAdmin(admin.ModelAdmin):

    def get_text(self, obj):
        return obj.text[:10]
    get_text.short_term = "text"
    list_display = ('from_user', 'to_user', 'date_create', 'get_text', 'task')

class InlineFiles(admin.TabularInline):
	model = DirectoryFile
	extra = 1

class DirectoryAdmin(tree_editor.TreeEditor):
	inlines = [InlineFiles, ]

# Re-register UserAdmin
admin.site.register(ShopSign)
admin.site.register(Shop)
admin.site.register(Task)
admin.site.register(Department)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Product)
admin.site.register(Feedback)
admin.site.register(Requests)
admin.site.register(Directory, DirectoryAdmin)
