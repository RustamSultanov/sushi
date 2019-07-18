from django import forms


from mickroservices.models import ScheduleModel


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = ('date_schedule', 'url_lesson')
        widgets = {
            'date_schedule': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1',
                'placeholder': "Даты занятий",
                })
        }
