from django import forms
from django.core.validators import EmailValidator
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from mickroservices.models import IdeaModel

class IdeaForm(forms.ModelForm):
    email = forms.CharField(validators=[EmailValidator])
    class Meta:
        model = IdeaModel
        exclude = ['status','answer','date_answer', 'date_created', ]
        widgets = {
            'body': forms.Textarea(attrs={'rows':2}),
        }