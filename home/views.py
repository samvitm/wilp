# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Permission,Group, User

from coordinator.forms import BitsCoordinatorForm
from coordinator.models import CompanyCoordinator
from wilp.coordinator.models import CoordManaged
from wilp.semester.models import Semester
from wilp.home.forms import SettingsForm,ImportForm
from wilp.coordinator.models import BitsCoordinator
from wilp.home.models import Import
from wilp.company.models import Company,Place
from wilp.programme.models import ProrammeSem,Programme
from wilp.faculty.models import Faculty,FacultySem
from wilp.courses.models import Course
from wilp.coordinator.forms import BitsCoordinatorForm

def get_company(s):
    try:
      c = Company.objects.get(name = str(s[1]).strip(),place__place = str(s[0]).strip())
      return c
    except :
      return Company.objects.get(name__exact = 'Dummy')



def home(request):
  if request.user.is_authenticated():
    return HttpResponseRedirect(reverse('profile'))
  else:
    return render_to_response('homepage.html',context_instance=RequestContext(request))
  
def page(request):
  return render_to_response('base.html')
@csrf_protect
def coord_settings(request):
  if request.POST:
    form = SettingsForm(request.POST)
    if form.is_valid():
      access = form.cleaned_data['access']
      companies = form.cleaned_data['companies']
      data = form.cleaned_data['data']
      
      if access:
        BitsCoordinator.objects.update(is_active = True)
      else:
        BitsCoordinator.objects.update(is_active = False)
      
      if companies:
        perm = Permission.objects.get(codename = 'can_add_companies')
        coords = BitsCoordinator.objects.all() 
        for coord in coords:
          coord.user_permissions.add(perm)
      else :
        perm = Permission.objects.get(codename = 'can_add_companies')
        coords = BitsCoordinator.objects.all() 
        for coord in coords:
          coord.user_permissions.remove(perm)

      if data:
        edit = Group.objects.get(name = 'Add content' )
        coords = BitsCoordinator.objects.all()
        for coord in coords:
          coord.groups.add(edit)
      else:
        edit = Group.objects.get(name = 'Add content' )
        coords = BitsCoordinator.objects.all()
        for coord in coords:
          coord.groups.remove(edit)
          
        
      messages.success(request,"Settings have been saved")
      return HttpResponseRedirect('/admin/')
    else:
      messages.error(request,"Some error has occures,please try again later")    
      return render_to_response('settings.html',{'form':form},context_instance=RequestContext(request))
        
  access = len(BitsCoordinator.objects.filter(is_active = True))
  perm = Permission.objects.get(codename = 'can_add_companies')
  coord = BitsCoordinator.objects.all()[:1].get()
  data = {}
  data['companies'] = coord.has_perm('coordinator.can_add_companies')
  data['data'] = coord.has_perm('faculty.add_faculty')
  if access > 0:
    data['access'] = True
  else :
    data['access'] = False
    
  form = SettingsForm(data)
  return render_to_response('settings.html',{'form':form},context_instance=RequestContext(request))

@login_required
def profile(request):

  try:
    coord = BitsCoordinator.objects.get(pk = request.user)
    return render_to_response('profile.html',{'coord':coord},context_instance=RequestContext(request))
  except :
    return render_to_response('profile.html',context_instance=RequestContext(request))


@login_required
@csrf_protect
def editprofile(request):
  if request.POST:
    try:
      coord = BitsCoordinator.objects.get(pk = request.user)
    except :
      raise Http404
    form = BitsCoordinatorForm(request.POST,instance=coord)
    if form.is_valid():
      form.save()
      message = "Details successfully updated."
      return render_to_response('editprofile.html',{'form':form,'message':message},context_instance=RequestContext(request))
    else:
      return render_to_response('editprofile.html',{'form':form},context_instance=RequestContext(request))

  try:
    coord = BitsCoordinator.objects.get(pk = request.user)
    form = BitsCoordinatorForm(instance=coord)
    return render_to_response('editprofile.html',{'form':form},context_instance=RequestContext(request))
  except :
    raise Http404

@csrf_protect
def login(request):
    if request.user.is_authenticated() :
        return HttpResponseRedirect(reverse('profile'))
    if request.POST :
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username = username,password = password)
        if user is not None and user.is_active:
            auth.login(request,user)
            u = User.objects.get(username = username)
            return HttpResponseRedirect(reverse('profile'))
        else:
            message = 'User Does not exist/Wrong username-password !!!'
	    return render_to_response('homepage.html', {'message':message},context_instance=RequestContext(request))
    else:
       return render_to_response('homepage.html',context_instance=RequestContext(request))




def reports(request):
  return render_to_response('reports.html',context_instance=RequestContext(request))
def imports(request):
  form = ImportForm()
  if request.method == 'POST':
    
    if request.POST['type'] == 'bitscoords':
      import xlrd
      i = Import()
      i.file = request.FILES['file']
      i.save()
      print i
      from wilp.settings import MEDIA_ROOT
      path = MEDIA_ROOT+i.file.name
      book = xlrd.open_workbook(path)
      sh = book.sheet_by_index(0)

      for rx in range(sh.nrows):
        c = BitsCoordinator()
        c.username = sh.cell_value(rx,0)
        c.first_name  = ''.join(str(sh.cell_value(rx,1)).rsplit(' ',1)[:-1])
        c.last_name = ''.join(str(sh.cell_value(rx,1)).rsplit(' ',1)[-1:])
        c.email = sh.cell_value(rx,2)
        c.address = sh.cell_value(rx,3)
        c.fax = sh.cell_value(rx,4)
        c.gender = 'F' if str(sh.cell_value(rx,5))=="Female" else 'M'
        c.mobile = sh.cell_value(rx,6)
        c.phone = sh.cell_value(rx,7)
        c.previous_experience = sh.cell_value(rx,8)
        c.qualification = sh.cell_value(rx,9)
        c.set_password(str(c.username))
        try:
          c.save()
          
        except:
          pass
      messages.success(request,"Successfuly imported " + str(sh.nrows) + ' BITS Coordinators')
      return render_to_response('imports.html',{'form':form},context_instance=RequestContext(request))

    if request.POST['type'] == 'companies':
      import xlrd
      i = Import()
      i.file = request.FILES['file']
      i.save()
      print i
      from wilp.settings import MEDIA_ROOT
      path = MEDIA_ROOT+i.file.name
      book = xlrd.open_workbook(path)
      sh = book.sheet_by_index(0)
      for rx in range(sh.nrows):
        place = sh.cell_value(rx,0)
        cname = sh.cell_value(rx,1)
        try:
           p = Place.objects.get(place = place)
           c = Company()
           c.name = cname
           c.place = p
           try:
            c.save()
           except :
            pass
        except :
          p = Place()
          p.place = place
          p.save()
          c = Company()
          c.name = cname
          c.place = p
          try:
            c.save()
          except :
            pass

        c = Company.objects.get(name = cname,place=p)
        s = Semester.objects.get(current = True)
        s.companies.add(c)
        s.save()
        try:
          co = BitsCoordinator.objects.get(username = sh.cell_value(rx,2))
          try:
            cm = CoordManaged.objects.get(coord = co,semester = s)
            cm.companies.add(c)
          except:
            cm = CoordManaged()
            cm.semester = s
            cm.coord = co
            cm.save()
            cm.companies.add(c)
            cm.save()
        except :
          pass
      messages.success(request,"Successfuly imported " + str(sh.nrows) + ' companies')
      return render_to_response('imports.html',{'form':form},context_instance=RequestContext(request))
        
    if request.POST['type'] == 'faculty':
      import xlrd
      i = Import()
      i.file = request.FILES['file']
      i.save()
      from wilp.settings import MEDIA_ROOT
      path = MEDIA_ROOT+i.file.name
      book = xlrd.open_workbook(path)
      sh = book.sheet_by_index(0)
      for rx in range(sh.nrows):
        fac = Faculty()
        fac.fac_name = sh.cell_value(rx,0)

        programme = sh.cell_value(rx,1)
        try:
          prog = Programme.objects.get(name__exact = programme)
        except :
          prog = Programme()
          prog.name = programme
          prog.save()

        company = str(sh.cell_value(rx,2)).split('-')
        print company
        c = get_company(company)
        print c
        if company != None:
          try:
            ps = ProrammeSem.objects.get(programme = prog)
            ps.company.add(c)
            ps.save()
          except :
            ps = ProrammeSem()
            ps.programme = prog
            ps.semester = Semester.objects.get(current = True)
            ps.save()
            if c:
              ps.company.add(c)
            ps.save()

        corse = str(sh.cell_value(rx,3)).split(' ',3)
        print  corse
        
        try:
          course = Course.objects.get(code = corse[2])
          try:
            pcs = prog.courses.all()
            if course not in pcs:
              prog.courses.add(course)
              prog.save()
          except :
            prog.courses.add(course)
        except :
          course = Course()
          course.name = corse[3]
          course.code = corse[2]
          course.cat = corse[1]
          course.save()
          prog.courses.add(course)
          prog.save()

        fac.email = sh.cell_value(rx,5)
        fac.phone = sh.cell_value(rx,15)
        fac.mobile = sh.cell_value(rx,11)
        fac.pan_no = sh.cell_value(rx,14)
        fac.gender = sh.cell_value(rx,9)
        fac.highest_degree = sh.cell_value(rx,10)
        fac.expertise_area = sh.cell_value(rx,7)
        fac.indus_exp = sh.cell_value(rx,17)
        fac.teach_exp = sh.cell_value(rx,19)
        fac.curr_aff = sh.cell_value(rx,4)
        fac.hrs = 0
        fac.bank_acc = sh.cell_value(rx,18)
        fac.dd = sh.cell_value(rx,20)
        fac.save()

        fs = FacultySem()
        fs.faculty = fac
        if c:
          fs.company = c
        fs.programme = prog
        fs.semester = Semester.objects.get(current = True)
        fs.course = course
        fs.batch_no = sh.cell_value(rx,6)
        fs.section_no = sh.cell_value(rx,16)
        fs.no_of_students = sh.cell_value(rx,13)
        fs.hrs_expected = sh.cell_value(rx,12)
        fs.honorarium = 100
        fs.honorarium_final = 100
        fs.save()

      messages.success(request,"Successfuly imported " + str(sh.nrows) + ' facultys')
      return render_to_response('imports.html',{'form':form},context_instance=RequestContext(request))

    if request.POST['type'] == 'companycoord':
      import xlrd
      i = Import()
      i.file = request.FILES['file']
      i.save()
      from wilp.settings import MEDIA_ROOT
      path = MEDIA_ROOT+i.file.name
      book = xlrd.open_workbook(path)
      sh = book.sheet_by_index(0)
      for rx in range(sh.nrows):
        c = CompanyCoordinator()
        company = str(sh.cell_value(rx,1)).split('-')
        c.name = str(sh.cell_value(rx,0))
        c.address = str(sh.cell_value(rx,2))
        c.email = str(sh.cell_value(rx,3))
        c.phone = str(sh.cell_value(rx,4))
        c.company = get_company(company)
        bc = CoordManaged.objects.get(companies=get_company(company))
        c.author = bc.coord
        c.save()
        c.semester.add(Semester.objects.get(current=True))
        c.save()
    messages.success(request,"Successfuly imported " + str(sh.nrows) + ' company coordinators')
    return render_to_response('imports.html',{'form':form},context_instance=RequestContext(request))




  else:
    return render_to_response('imports.html',{'form':form},context_instance=RequestContext(request))
