from django import forms


from mickroservices.models import NewsPage
from quill.fields import RichTextField


class NewsForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.HiddenInput())
    content = forms.CharField(widget=forms.HiddenInput())
    first_published_at = forms.DateField(
        input_formats=["%d %b %Y %H:%M:%S %Z"],
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
        model = NewsPage
        fields = ('title', 'first_published_at', 'body', 'content')
