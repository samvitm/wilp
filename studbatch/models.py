from django.db import models
from wilp.company.models import Company
from wilp.programme.models import Programme
from wilp.semester.models import Semester
from smart_selects.db_fields import ChainedForeignKey 
# Create your models here.

class StudentBatch(models.Model):
  company = models.ForeignKey(Company)
  programme = models.ForeignKey(Programme)
  semester = models.ForeignKey(Semester)
  batch = models.ForeignKey('BatchYear')
  sem = models.ForeignKey('Sem')
  males = models.IntegerField(verbose_name = 'No of males Onrolls')
  females = models.IntegerField(verbose_name = 'No of females Onrolls')
  reg_male = models.IntegerField(verbose_name = 'No of males registered')
  reg_female = models.IntegerField(verbose_name = 'No of females registered')
  
  def __unicode__(self):
    return str(self.programme) + ' - '+ str(self.batch) + ' '+str(self.sem) + ' semester' 
  
   
  
class BatchYear(models.Model):
  batch_year = models.IntegerField()
  
  def __unicode__(self):
    return str(self.batch_year)

 
  
class Sem(models.Model):
  sem = models.CharField(max_length = 100, verbose_name = 'Semester')
  
  def __unicode__(self):
    return self.sem
  
 
