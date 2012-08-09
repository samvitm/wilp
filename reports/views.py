# Create your views here.
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from wilp.company.models import Company
from wilp.programme.models import Programme

def basic(request):
  companies = Company.objects.all()
  progs = Programme.objects.all()
  return render_to_response('report_base.html',{'progs' : progs, 'companies':companies },context_instance=RequestContext(request))



  
