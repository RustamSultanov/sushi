from .models import Messeges, Feedback
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#from django_registration.forms import RegistrationForm
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

User = get_user_model()

# class RegistrationCustomForm(RegistrationForm):
#     class Meta(RegistrationForm.Meta):
#         model = User
#         fields = [
#             User.USERNAME_FIELD,
#             'first_name',
        
#         ]
#         widgets = {
#             User.USERNAME_FIELD : PhoneNumberInternationalFallbackWidget(attrs={'id':"email", 'class':"validate"}),
#         }
#     def __init__(self, *args, **kwargs):
#         super(RegistrationCustomForm, self).__init__(*args, **kwargs)
#         # email_field = User.get_email_field_name()
#         # self.fields[email_field].required = False

#     def save(self,commit=False):
#         user = super(R
    # password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Повторите пароль', 'name' : 'password_check'}))

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
               'class': "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control"}))



class MessegesForm(forms.ModelForm):

    class Meta:
        model = Messeges
        fields = ['text']
        widgets = {
                'text': forms.TextInput(attrs={'id' : 'message', 'class' : 'mdc-text-field__input'})
                }

class FeedbackForm(forms.ModelForm):
    class Meta:
            model = Feedback
            fields = ['text', 'rating', 'files', 'adv', 'disadv', ]
            widgets = {
                'text': forms.Textarea(attrs={'id':"textarea-3",'class':"mdc-text-field__input", 'rows' : '4','cols':"40"}),
                'adv': forms.Textarea(attrs={'id':"textarea-1",'class':"mdc-text-field__input", 'rows' : '4','cols':"40"}),
                'disadv': forms.Textarea(attrs={'id':"textarea-2",'class':"mdc-text-field__input",' name':"rating", 'rows' : '4','cols':"40"}),
                'rating': forms.RadioSelect(attrs={'class':"input-hidden",' name':"rating"}),
                'files': forms.ClearableFileInput(attrs={'id':"file",'class':"input-hidden",}),
            }

