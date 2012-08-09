from django.contrib import admin
from wilp.company.models import Place,Company

class CompanyAdmin(admin.ModelAdmin):
  list_display = ['place','name']
  list_display_links = ['name']

admin.site.register(Place)
admin.site.register(Company,CompanyAdmin)


