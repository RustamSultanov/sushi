from .models import Messeges, Feedback, Requests, Task, UserProfile
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.db import models
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django_registration.forms import RegistrationForm
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
            'text': forms.TextInput(attrs={'id': 'message', 'class': 'mdc-text-field__input'})
        }


class RequestsForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={'name': 'title', 'class': 'form-control', 'placeholder': "Название запроса"}),
            'description': forms.Textarea(
                attrs={'placeholder': "Описание запроса", 'class': "form-control"}),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(
                attrs={'name': 'title', 'class': 'form-control', 'placeholder': "Название задачи"}),
            'description': forms.Textarea(
                attrs={'placeholder': "Описание задачи", 'class': "form-control"}),
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['source', 'description', 'date_pub', 'shop']
        widgets = {
            'source': forms.TextInput(
                attrs={'placeholder': "Источник отзыва", 'class': "form-control"}),
            'description': forms.Textarea(
                attrs={'placeholder': "Текст отзыва", 'class': "form-control", 'rows': '2'}),
            'date_pub': forms.DateInput(
                attrs={'id': "b-m-dtp-date", 'class': "form-control", 'placeholder': "Выберите дату"}),
            'shop': forms.Select(attrs={'class': "select2 form-control"}),
        }


class RegistrationEmployeeMainForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 'password'
        ]

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', }),
            'first_name': forms.TextInput(attrs={'class': 'form-control', }),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', })
        }

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с такой почтой уже зарегистрирован')
        password_check = self.cleaned_data['password_check']
        password = self.cleaned_data['password']
        if password_check != password:
            raise forms.ValidationError('Пароль не совпадает!')


class RegistrationEmployeeAdditionForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = [
            'head', 'manager', 'is_head', 'is_partner', 'is_manager', 'wagtail_profile', 'user'
        ]
        widgets = {
            'phone_number': PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control', }),
            'whatsapp': PhoneNumberInternationalFallbackWidget(attrs={'class': 'form-control', }),
            'twitter': forms.URLInput(attrs={'class': 'form-control', }),
            'facebook': forms.URLInput(attrs={'class': 'form-control', }),
            'instagram': forms.URLInput(attrs={'class': 'form-control', }),
            'middle_name': forms.TextInput(attrs={'class': 'form-control', }),
            'position': forms.TextInput(attrs={'class': 'form-control', }),

        }
