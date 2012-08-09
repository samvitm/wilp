# Create your views here.

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from wilp.coordinator.models import BitsCoordinator
from wilp.company.models import Company
from wilp.semester.models import Semester
from wilp.faculty.forms import FacultySemForm,FacultyForm,FacultySemForm2
from wilp.faculty.models import Faculty,FacultySem
from wilp.coordinator.models import CoordManaged


def addfaculty(request):
  sform = FacultySemForm()
  sform.fields["company"].queryset = Company.objects.filter(coordmanaged__coord__id = request.user.id)
  if request.POST:
    if request.POST.has_key('submit1'):
      pan = request.POST['pan_no']
      try:
        fac = Faculty.objects.get(pan_no = pan)
        fform = FacultyForm(instance=fac)
        message = 'Faculty with given PAN number has been found, you may edit the details below'
      except ObjectDoesNotExist:
        fform = FacultyForm()
        message = 'Faculty with given PAN does not exist in the database, please fill in the details below.'
      sform2 = FacultySemForm2(request.POST)
      return render_to_response('fac_add.html',{'sform2':sform2,'fform':fform,'message':message},context_instance=RequestContext(request))
    elif request.POST.has_key('submit2'):
      sform2 = FacultySemForm2(request.POST)
      fform = FacultyForm(request.POST)
      if sform2.is_valid() and fform.is_valid():
        fs = sform2.save(commit=False)
        try:
          fac = Faculty.objects.get(pan_no = request.POST['pan_no'])
          fform = FacultyForm(request.POST, instance = fac)
        except ObjectDoesNotExist:
          fform = FacultyForm(request.POST)

        f = fform.save(commit=False)
        f.author = BitsCoordinator.objects.get(pk = request.user.id)
        f.save()

        fs.faculty = f;
        fs.semester = Semester.objects.get(current=True)
        fs.save()
        message = 'Faculty details have been saved'
        return render_to_response('fac_add.html',{'sform':sform,'message':message},context_instance=RequestContext(request))
      else:
        message = 'Please correct the errors below'
        return render_to_response('fac_add.html',{'sform2':sform2,'fform':fform,'message':message},context_instance=RequestContext(request))
  return render_to_response('fac_add.html',{'sform':sform},context_instance=RequestContext(request))

@login_required
def viewfacs(request):
  fs = FacultySem.objects.filter(faculty__author__id = request.user.id,semester__current = True)
  return render_to_response('view_facs.html',{'facs':fs},context_instance=RequestContext(request))