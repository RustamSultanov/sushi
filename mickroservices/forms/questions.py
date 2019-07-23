from django import forms
from django.core.validators import EmailValidator

from mickroservices.models import QuestionModel

class QuestionForm(forms.ModelForm):
    email = forms.CharField(validators=[EmailValidator])

    class Meta:
        model = QuestionModel
        exclude = ['name','status','answer',]
        widgets = {
            'body': forms.Textarea(attrs={'rows':5}),
        }