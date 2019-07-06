from django.contrib import admin

from .models import (QuestionModel,TypeCourseModel, CourseModel, PlanDayModel,
                     ScheduleModel,)

admin.site.register(QuestionModel)
admin.site.register(TypeCourseModel)
admin.site.register(CourseModel)
admin.site.register(PlanDayModel)
admin.site.register(ScheduleModel)
