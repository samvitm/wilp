from django.db import models
from wilp.company.models import Company
from wilp.programme.models import Programme
from wilp.courses.models import Course
from wilp.semester.models import Semester
from wilp.coordinator.models import BitsCoordinator
from smart_selects.db_fields import ChainedForeignKey
# Create your models here.

class Faculty(models.Model):
  fac_name = models.CharField(max_length = 100, verbose_name = 'Faculty Name')
  email = models.EmailField()
  phone = models.CharField(max_length = 40)
  mobile = models.CharField(max_length = 40)
  pan_no = models.CharField(max_length = 40, blank = True, null = True)
  gender = models.CharField(max_length = 1000, choices = (('male','Male'),('female','Female')))
  highest_degree = models.CharField(max_length = 1000, blank = True, null = True)
  expertise_area = models.CharField(max_length = 1000, blank = True, null = True)
  indus_exp = models.CharField( max_length = 1000,verbose_name = 'Years of Industry experience', blank = True, null = True)
  teach_exp = models.CharField( max_length = 1000,verbose_name = 'Years of Teaching experience', blank = True, null = True)
  curr_aff = models.CharField(max_length = 1000,verbose_name = 'Current Affilation (Designation & Organisation)', blank = True, null = True)
  hrs = models.CharField(max_length = 1000,verbose_name = 'No of hours expected', blank = True, null = True)
  bank_acc = models.CharField(max_length = 1000, verbose_name = 'Bank account number', blank = True, null = True)
  dd = models.CharField( max_length = 1000, verbose_name = 'DD payable at')
  author = models.ForeignKey(BitsCoordinator,null=True,blank=True)
  
  
  def __unicode__(self):
    return str(self.fac_name)


class FacultySem(models.Model):
  faculty = models.ForeignKey(Faculty)
  company = models.ForeignKey(Company)
  programme = models.ForeignKey(Programme)
  semester = models.ForeignKey(Semester)
  course = models.ForeignKey(Course)
  batch_no = models.CharField(max_length = 40)
  section_no = models.CharField(max_length = 40)
  no_of_students = models.CharField(max_length = 40)
  hrs_expected = models.CharField(max_length = 40,verbose_name = 'No of hours expected to be handled', blank = True, null = True)
  honorarium = models.CharField(max_length = 40,verbose_name = 'Honorarium amount to be paid', blank = True, null = True)
  honorarium_final = models.CharField(max_length = 40,verbose_name = 'Final honorarium amount' , blank = True, null = True)

  def __unicode__(self):
    return str(self.faculty) + " - " + str(self.company) + " - " + str(self.programme)
