# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from wilp.studbatch.models import StudentBatch
from wilp.studbatch.forms import StudbatchForm
from wilp.company.models import Company
from wilp.semester.models import Semester

@login_required
@csrf_protect
def addstudbatch(request):
  form = StudbatchForm()
  coms =  Company.objects.filter(coordmanaged__coord__id = request.user.id)
  form.fields["company"].queryset = coms
  form.fields["semester"].queryset = Semester.objects.filter(current=True)
  studs = StudentBatch.objects.filter(company__in = coms)
  if request.POST:
    form = StudbatchForm(request.POST)
    if form.is_valid():
      form.save()
      message = 'Student Batch has been saved'
      form.fields["company"].queryset = Company.objects.filter(coordmanaged__coord__id = request.user.id)
      form.fields["semester"].queryset = Semester.objects.filter(current=True)
      return render_to_response('studbatch.html',{'form':form,'message':message,'studs':studs},context_instance=RequestContext(request))
    else:
      message = 'Please fix the errors below'
      form.fields["company"].queryset = Company.objects.filter(coordmanaged__coord__id = request.user.id)
      form.fields["semester"].queryset = Semester.objects.filter(current=True)
      return render_to_response('studbatch.html',{'form':form,'message':message,'studs':studs},context_instance=RequestContext(request))
  return render_to_response('studbatch.html',{'form':form,'studs':studs},context_instance=RequestContext(request))

@login_required
def viewstuds(request):
  coms =  Company.objects.filter(coordmanaged__coord__id = request.user.id)
  studlist = StudentBatch.objects.filter(company__in = coms)
  print studlist
  return render_to_response('view_studs.html',{'studlist':studlist},context_instance=RequestContext(request))