from django.contrib import admin
from wilp.courses.models import Course

class CourseAdmin(admin.ModelAdmin):
  list_filter = ('code',)


admin.site.register(Course,CourseAdmin)

