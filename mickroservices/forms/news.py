from django import forms


from mickroservices.models import NewsPage
from quill.fields import RichTextField


class NewsForm(forms.Form):
    title = forms.CharField()
    body = RichTextField(blank=True)
    first_published_at = forms.DateField(
        localize=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'placeholder': "Даты занятий",
            'wtype': 'date',
            'type': 'text'
        })
    )

    class Meta:
        fields = ('title', 'first_published_at', 'body')
