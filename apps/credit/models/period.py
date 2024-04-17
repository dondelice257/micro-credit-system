from django.db import models

# Create your models here.
class Period(models.Model):
  value = models.IntegerField()
  name = models.CharField(max_length=255)
