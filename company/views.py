# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from coordinator.models import BitsCoordinator
from wilp.semester.models import Semester
from wilp.company.models import Company
from wilp.coordinator.models import CoordManaged
from django.db.models import Count
from wilp.company.forms import CompanyForm

@login_required
@csrf_protect
def advcompanies(request):
  cmd = CoordManaged.objects.filter(coord__id = request.user.id)
  try:
    cmds = cmd.get(semester__current = True)
  except :
    cmds = CoordManaged()
    cmds.semester = Semester.objects.get(current = True)
    cmds.coord = BitsCoordinator.objects.get(pk = request.user.id)
    cmds.save()
  
  if request.user.has_perm('coordinator.can_add_companies'):
    form = CompanyForm(instance=cmds)
  else:
    form = ''
  coms = cmd
  if request.POST:
    form = CompanyForm(request.POST,instance=cmds)
    if form.is_valid():
      if request.user.has_perm('coordinator.can_add_companies'):
        form.save()
        message = 'Companies have been saved'
      else:
        message = 'You do not have permissions to edit.'
      return render_to_response('companies.html',{'form':form,'companies':coms,'message':message},context_instance=RequestContext(request))

  #coms = Company.objects.select_related().filter(coordmanaged__coord__id = request.user.id)
  return render_to_response('companies.html',{'form':form,'companies':coms},context_instance=RequestContext(request))

