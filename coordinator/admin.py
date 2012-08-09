from django.contrib import admin
from wilp.coordinator.models import BitsCoordinator,CompanyCoordinator,CoordManaged
from django.forms.widgets import PasswordInput
from wilp.semester.models import Semester
from django.contrib.auth.models import Group

class CompanyCoordinatorAdmin(admin.ModelAdmin):

  filter_horizontal = ['semester']
  list_display = ['name','company','phone','email','address']
  list_filter = ('company','semester',)
  change_list_template = 'report_comcoord.html'
  def save_model(self,request,obj,form,change):
    if getattr(obj,'author',None) is None:
      obj.author = request.user
    obj.last_modified_by = request.user
  def queryset(self , request):
    qs = super(CompanyCoordinatorAdmin, self).queryset(request)
    if request.user.is_superuser:
        return qs
    return qs.filter(author = request.user)


def createpass(passw):
  from hashlib import sha1
  import random
  import string
  ran = str(''.join(random.sample(string.letters,5)))
  hex = sha1(ran + str(passw))
  hex = hex.hexdigest()
  passw = "sha1$" + ran +"$" + hex
  return  passw
  


class BitsCoordinatorAdmin(admin.ModelAdmin):

  def queryset(self , request):
    qs = super(BitsCoordinatorAdmin , self).queryset(request)
    if request.user.is_superuser:
        return qs
    return qs.filter(pk = request.user)

  def get_form(self, request, obj=None, **kwargs):
    """
    Handling the form based on permissions of the BITS coordinator.
    """
    id = request.user
    if request.user.is_superuser:
      return super(BitsCoordinatorAdmin, self).get_form(request, obj=None, **kwargs)
    try :
      coord = BitsCoordinator.objects.get( pk = request.user )
      if coord.has_perm('coordinator.can_add_companies'):
        self.exclude = ( 'is_superuser','last_login','date_joined','user_permissions','groups','semester','password','is_staff','username','is_active')
      else:
        self.exclude = ( 'is_superuser','last_login','date_joined','user_permissions','groups','semester','companies','password','is_staff','username','is_active')

    except :
      self.exclude = ( 'is_superuser','last_login','date_joined','user_permissions','groups','semester','companies','is_staff')
    return super(BitsCoordinatorAdmin, self).get_form(request, obj=None, **kwargs)

  def semesters(self,c):
    sems = c.semester.all()
    s = ''
    for sem in sems:
      s+= str(sem)+','
    return s[:-1]

  def companyes(self,c):
    coms = c.companies.all()
    s = ''
    for com in coms:
      s+= str(com)+','
    return s[:-1]
  companyes.short_description = 'Companies managed'



  def formfield_for_dbfield(self, db_field,**kwargs):
    if db_field.name == 'password':
        kwargs['help_text'] = None
    return super(BitsCoordinatorAdmin,self).formfield_for_dbfield(db_field,**kwargs)

  def fullname(self,c):
    return c.get_full_name()
  #exclude = ( 'is_superuser','last_login','date_joined','user_permissions','groups','semester',)
  list_display = ('username','fullname','email','gender','mobile','qualification',)

  def save_model(self,request,obj,form,change):
    if obj.id:
      print 'This has an id'
    else:
      print 'New one!'
      obj.password = createpass(form.cleaned_data['password'])
      obj.save()
  
class CoordManagedAdmin(admin.ModelAdmin):

  change_list_template = 'report_bitscoord.html'
  def name(self,cm):
    link = '<a href="../bitscoordinator/'+ str(cm.coord.id) + '">'
    n = cm.coord.get_full_name()
    if not n:
      n = '--Not Given--'
    link+=str(n)
    link+='</a>'
    return link
  name.allow_tags = True
  def comps(self,ps):
    cs = ps.companies.all()
    s = '<ul>'
    for c in cs:
      s+='<li>'+str(c)+'</li>'
    s+='</ul>'
    return s
  comps.short_description = 'Companies'
  comps.allow_tags = True
  list_display = ['coord','name','semester','comps']
  list_filter = ['semester','coord','companies']
  filter_horizontal = ['companies']


admin.site.register(CompanyCoordinator,CompanyCoordinatorAdmin)
admin.site.register(BitsCoordinator,BitsCoordinatorAdmin)
admin.site.register(CoordManaged,CoordManagedAdmin)
