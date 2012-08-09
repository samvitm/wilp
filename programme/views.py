# Create your views here.
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.utils import simplejson
from wilp.courses.models import Course
from wilp.programme.models import ProrammeSem

def getprogs(request):
  if request.is_ajax():
    c = request.GET['company']
    ps = ProrammeSem.objects.values('programme','programme__name').filter(company__id=c,semester__current=True)
    psl = []
    for p in ps:
      psl.append([p['programme'],p['programme__name']])
    json = simplejson.dumps(psl)
    return HttpResponse(json, mimetype='application/json')
  raise Http404


def getcourses(request):
  if request.is_ajax():
    p = request.GET['programme']
    cs = Course.objects.filter(programme__id = p)
    csl = []
    for c in cs:
      csl.append([c.id,str(c)])
    json = simplejson.dumps(csl)
    return HttpResponse(json, mimetype='application/json')
  raise Http404