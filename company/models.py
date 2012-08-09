from django.db import models
# Create your models here.

class Place(models.Model):
  place = models.CharField(max_length = 100)
  
  def __unicode__(self):
    return str(self.place)

class Company(models.Model):
  name = models.CharField(max_length = 100,verbose_name ='Name')
  place = models.ForeignKey(Place)
  
  def __unicode__(self):
    return self.name + ' - ' + str(self.place)


    
  class Meta:
    verbose_name_plural = 'Companies'
    unique_together = ("name", "place")
