from wilp.semester.models import Semester,AcademicYear
from django.contrib import admin

class Foo:
  def __call__(self,shit,moreshit):
    pass
  
class SemesterAdmin(admin.ModelAdmin):
  readonly_fields = ('current',)
  filter_horizontal = ['companies']
  list_filter = ['current']
  list_display = ['semester','current','comps']
  fields = ('academic_year','sem','current','companies')
  def comps(self,ps):
    cs = ps.companies.all()
    s = '<ul style="">'
    for c in cs:
      s+='<li>'+str(c)+'</li>'
    s+='</ul>'
    return s
  comps.short_description = 'Companies'
  comps.allow_tags = True

  def setcurr(self,request,queryset):
    if len(queryset)>1:
      from django.contrib import messages
      messages.error(request,'More than 1 semester is selected, please select only 1 semester')
      self.message_user = str()
    else:
      sem = Semester.objects.all()
      sem.update(current = False)
      queryset.update(current = True)
      self.message_user(request,"Current semester is set")
  setcurr.short_description = 'Set as current semester'

  actions = [setcurr]
        
  ordering = ('-current',)


  def semester(self,s):
    return str(s.sem) + ' semester : ' + str(s.academic_year)
  semester.short_description = 'Semester'




admin.site.register(Semester,SemesterAdmin)
admin.site.register(AcademicYear)
