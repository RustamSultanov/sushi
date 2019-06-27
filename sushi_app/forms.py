from .models import Messeges, Feedback
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField
#from django_registration.forms import RegistrationForm
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone_number',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone_number', 'password','first_name','last_name' , 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



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
#         user = super(RegistrationCustomForm, self).save(commit=False) 
#         user.save() 
#         return user

class RegistrationCustomForm(forms.ModelForm):
    # password_check = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder' : 'Повторите пароль', 'name' : 'password_check'}))
    class Meta:
        model = User
        fields = ['phone_number', 'first_name']
        widgets = {
        'phone_number' : PhoneNumberInternationalFallbackWidget(attrs={'id' : 'phone', 'class' : 'mdc-text-field__input'}),
        'first_name' : forms.TextInput(attrs={'id' : 'name', 'class' : 'mdc-text-field__input'}),
        
    
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
               'class': "form-control"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': "form-control"}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'profile_picture']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'last_name': forms.TextInput(attrs={'class': 'form-control', }),
            'profile_picture': forms.FileInput()
        }

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

