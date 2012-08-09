from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from wilp.home.views import *
from wilp.faculty.views import *
from wilp.programme.views import *
from wilp.company.views import *
from wilp.coordinator.views import *
from wilp.studbatch.views import *
from django.contrib.auth.views import logout
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$',home,name='home'),
    url(r'^page/$',page,name='page  '),
    url(r'^logout/$',logout,{'template_name':'logout.html'},name ='logout'),
    url(r'^login/$',login,name='login'),
    url(r'^profile/$',profile,name='profile'),
    url(r'^editprofile/$',editprofile,name='editprofile'),
    url(r'^settings/$',coord_settings,name = 'settings'),
    url(r'^imports/$',imports,name='imports'),
    url(r'^reports/$',reports,name='reports'),
    url(r'^chaining/', include('smart_selects.urls')),

    url(r'^admin/', include(admin.site.urls),name = 'admin'),
    
     (r'^static/(?P<path>.*)$','django.views.static.serve',
         {'document_root': 'c:/Users/Ednha/wilp/static'}),
    
    
)


urlpatterns+=patterns('',

  url(r'^addfaculty/$',addfaculty,name='addfaculty'),
  url(r'^viewfaculty/$',viewfacs,name='viewfacs')

)

urlpatterns+=patterns('',

  url(r'^get_progs/$',getprogs),
  url(r'^get_courses/$',getcourses),

)

urlpatterns+=patterns('',

  url(r'^companies/$',advcompanies,name='advcompanies'),

)


urlpatterns+=patterns('',

  url(r'^companycoord/$',company_coord,name='companycoord'),
  url(r'^viewcompanycoords',viewcomcoords,name='viewcomcoords')

)

urlpatterns+=patterns('',

  url(r'^addstudbatch/$',addstudbatch,name='addstudbatch'),
  url(r'^studbatch/$',viewstuds,name='viewstuds'),

)

from wilp.studbatch.models import StudentBatch
from wilp.faculty.models import Faculty
from wilp.seeker.plugins.model import ModelSearchPlugin



urlpatterns+= patterns('',
    ( r'^search/', include('wilp.seeker.urls'), params ),

)
