from django.contrib.auth import views as auth_views
from .forms import ResetUserForm,ConfurmResetUserForm

class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'password/reset_login.html'
    form_class = ResetUserForm
    

class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name='password/password_reset_done.html'

class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "password/password_reset_confirm.html"
    form_class = ConfurmResetUserForm

class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name='password/password_reset_complete.html'
