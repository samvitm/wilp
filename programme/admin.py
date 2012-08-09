from django.contrib import admin
from wilp.programme.models import Programme,ProrammeSem

class ProgrammeAdmin(admin.ModelAdmin):
  def course(self,p):
    cs = p.courses.all()
    s = '<ul>'
    for c in cs:
      s+='<li>'+str(c)+'</li>'
    s+='</ul>'
    return s
  course.short_description = 'Courses Included'
  course.allow_tags = True

  list_display = ('name','course',)
  filter_vertical = ('courses',)


class ProgrammeSemAdmin(admin.ModelAdmin):
  def comps(self,ps):
    cs = ps.company.all()
    s = '<ul>'
    for c in cs:
      s+='<li>'+str(c)+'</li>'
    s+='</ul>'
    return s
  change_list_template = 'report_programme.html'
  comps.short_description = 'Companies'
  comps.allow_tags = True
  list_display = ('programme','semester','comps',)
  list_filter = ('programme','company','semester',)

admin.site.register(Programme,ProgrammeAdmin)
admin.site.register(ProrammeSem,ProgrammeSemAdmin)
