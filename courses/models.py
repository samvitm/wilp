from django.db import models

# Create your models here.


class Course(models.Model):
  cat = models.CharField(max_length = 100, verbose_name = 'Category')
  code = models.CharField(max_length = 100, verbose_name = 'Course Code')
  name = models.CharField(max_length = 100, verbose_name = 'Course name')
  
  def __unicode__(self):
    return self.cat+' '+self.code+' '+self.name
  
