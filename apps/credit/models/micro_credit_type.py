from django.db import models

# Create your models here.


class MicroCreditType(models.Model):
  slug = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
  mode = models.CharField(max_length=255)