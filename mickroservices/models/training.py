from django.conf import settings
from django.db import models



class TypeCourseModel(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Название')
    
    class Meta:
        verbose_name = 'Тип курса'
        verbose_name_plural = 'Типы курсов'
        ordering = ['title']

    def __str__(self):
        return self.title

class CourseModel(models.Model):
    """docstring for CourseModel"""

    title = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Название курса')
    description = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Оисание курса')
    
    class Meta:
        verbose_name = 'Курс обучения'
        verbose_name_plural = 'Курсы обучения'
        ordering = ['title']

    def __str__(self):
        return self.title


class PlanDayModel(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Название')
    body = models.CharField(max_length=1000, blank=False, null=False,
                            verbose_name='План')
    lecturer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 on_delete=models.CASCADE,
                                 verbose_name='Лектор',
                                 related_name='day_plans')
    type = models.ForeignKey(TypeCourseModel, verbose_name='типы курсов',
                             on_delete=models.CASCADE,
                             related_name='courses')
    address = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Адрес проведения')
    start_time = models.TimeField(verbose_name='Время начала')
    end_time = models.TimeField(verbose_name='Время окончания')

    class Meta:
        verbose_name = 'План дня'
        verbose_name_plural = 'Планы дней'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} {self.address}-{self.start_time}:{self.end_time}'

class ScheduleModel(models.Model):
    title = models.CharField(max_length=255, blank=False, null=False,
                            verbose_name='Название')
    date_schedule = models.DateTimeField(verbose_name='Дата проведения')
    number_day = models.PositiveSmallIntegerField(verbose_name='Порядновый номер дня проведения')
    plansday = models.ManyToManyField(PlanDayModel,
                                verbose_name='планы дня',
                                related_name='schedules')
    course = models.ForeignKey(CourseModel,
                                 on_delete=models.CASCADE,
                                 verbose_name='курс',
                                 related_name='schedule')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        ordering = ['date_schedule', 'number_day']

    def __str__(self):
        return f'{self.title}'