from django.db import models
from wilp.company.models import Company

# Create your models here.

class AcademicYear(models.Model):
  start = models.IntegerField()
  end = models.IntegerField()
  
  def __unicode__(self):
    return str(self.start) + ' - ' + str(self.end)


class Semester(models.Model):
  academic_year = models.ForeignKey(AcademicYear)
  sem = models.CharField( max_length = 10, choices = (('First','First'),('Second','Second')),verbose_name = 'Semester',)
  companies = models.ManyToManyField(Company,blank=True,null=True)
  current = models.NullBooleanField(blank=True,null=True)
  
  def __unicode__(self):
    return str(self.sem) + ' semester : ' + str(self.academic_year)
  
