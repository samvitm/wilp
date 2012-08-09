# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from wilp.coordinator.models import BitsCoordinator
from wilp.company.models import Company
from wilp.semester.models import Semester
from wilp.coordinator.models import CoordManaged,CompanyCoordinator
from wilp.coordinator.forms import CompanyCoordinatorForm

@login_required
@csrf_protect
def company_coord(request):
  form = CompanyCoordinatorForm()
  if request.POST:
    form = CompanyCoordinatorForm(request.POST)
    if form.is_valid():
      form = form.save(commit=False)
      form.author = BitsCoordinator.objects.get(pk = request.user.id)
      form.save()
      form.semester.add(Semester.objects.get( current = True))
      form.save()
      message = 'Company Coordinator added successfully!'
      form = CompanyCoordinatorForm()
      form.fields["company"].queryset = Company.objects.filter(coordmanaged__coord__id = request.user.id)
      return render_to_response('company_coord.html',{'form':form,'message':message},context_instance=RequestContext(request))
    else:
      form.fields["company"].queryset = Company.objects.filter(coordmanaged__coord__id = request.user.id)
      message = 'Please fix the errors below!'
      return render_to_response('company_coord.html',{'form':form,'message':message},context_instance=RequestContext(request))
  form.fields["company"].queryset = Company.objects.filter(coordmanaged__coord__id = request.user.id)
  return render_to_response('company_coord.html',{'form':form},context_instance=RequestContext(request))


def viewcomcoords(request):
  comcs = CompanyCoordinator.objects.filter(author__id = request.user.id,semester__current = True)
  return render_to_response('coordview.html',{'comcs':comcs},context_instance=RequestContext(request))
