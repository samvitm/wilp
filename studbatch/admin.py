from django.contrib import admin
from wilp.studbatch.models import StudentBatch,BatchYear,Sem
from wilp.semester.models import Semester

class Foo:
  def __call__(self,hit,rehit):
    pass

class StudentBatchAdmin(admin.ModelAdmin):
  #readonly_fields = ['semester']
  list_filter = ('semester','company','programme')
  list_display = ('company','programme','batch','sem',)#'males','females','reg_male','reg_female')
  #exclude = ('semester',)
  change_list_template = 'report_stud.html'
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == "semester":
      kwargs["queryset"] = Semester.objects.filter(current = True)
    return super(StudentBatchAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
  
  def save_model(self,request,obj,form,change):
    try :
      semester = Semester.objects.get(current = True)
      obj.semester = semester
      obj.save()
    except :
      from django.contrib import messages
      messages.error(request,'No current semester is set, please contact site administrator to set the current semester.')
      self.message_user = Foo()
    


admin.site.register(StudentBatch,StudentBatchAdmin)
admin.site.register(BatchYear)
admin.site.register(Sem)
