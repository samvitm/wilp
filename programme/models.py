from django.db import models
from wilp.courses.models import Course
from wilp.company.models import Company
from wilp.semester.models import Semester
# Create your models here.

class Programme(models.Model):
  name = models.CharField(max_length = 100,verbose_name = 'Name',unique=True)
  courses = models.ManyToManyField(Course)

  def __unicode__(self):
    return str(self.name)


class ProrammeSem(models.Model):
  programme = models.ForeignKey(Programme)
  company = models.ManyToManyField(Company)
  semester = models.ForeignKey(Semester)

  def __unicode__(self):
    return str(self.programme)