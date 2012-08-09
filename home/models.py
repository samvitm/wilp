from django.db import models

# Create your models here.
class Import(models.Model):
  file = models.FileField(upload_to='imports')

  def __unicode__(self):
    return self.file.name