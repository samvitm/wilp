from django.db import models
from django.contrib.auth.models import User
from wilp.company.models import Company
from wilp.semester.models import Semester
# Create your models here.

GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )


class BitsCoordinator(User):
  address = models.TextField(blank=True,null=True)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True,null=True)
  phone = models.CharField(max_length = 200,blank=True,null=True)
  mobile = models.CharField(max_length = 200,blank=True,null=True)
  fax = models.CharField(max_length = 20,blank=True,null=True)
  qualification = models.CharField(max_length = 300,blank=True,null=True)
  previous_experience = models.TextField(blank=True,null=True)
  
  class Meta:
    verbose_name = 'BITS Coordinator'
    
    permissions = (('can_add_companies','Can add managed companies'),)
  



class CoordManaged(models.Model):
  semester = models.ForeignKey(Semester)
  coord = models.ForeignKey(BitsCoordinator)
  companies = models.ManyToManyField(Company)

class CompanyCoordinator(models.Model):
  company = models.ForeignKey(Company)
  name = models.CharField(max_length = 100)
  semester = models.ManyToManyField(Semester,verbose_name = 'Semester(s)')
  address = models.TextField()
  designation = models.CharField(max_length = 100)
  gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
  phone = models.CharField(max_length = 20)
  mobile = models.CharField(max_length = 20)
  email = models.EmailField(unique = True)
  author = models.ForeignKey(BitsCoordinator)
  
  
  
  
  
  
