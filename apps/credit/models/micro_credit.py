from django.db import models
from apps.authentication.models import User
from .period import Period
from .micro_credit_type import MicroCreditType

# Create your models here.
class MicroCredit(models.Model):
  amount = models.FloatField()
  holder = models.ForeignKey(User, on_delete=models.CASCADE)
  created_at = models.DateField(auto_now_add=True)
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_microcredit')
  approved_at = models.DateField(blank=True, null=True)
  approved_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='approved_microcredit')
  cancelled_at = models.DateField(blank=True, null=True)
  cancelled_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='cancelled_microcredit')
  rejected_at = models.DateField(blank=True, null=True)
  rejected_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='rejected_microcredit')
  credit_type = models.ForeignKey(MicroCreditType, on_delete=models.SET_NULL, null=True)
  period = models.ForeignKey(Period, on_delete=models.SET_NULL, null=True)
  payment_date = models.DateField(blank=True, null=True)
  expiration_date = models.DateField(blank=True, null=True)
  delay_days = models.IntegerField(blank=True, null=True)
  interest_rate = models.FloatField(blank=True, null=True)
  penalities_rate = models.FloatField(blank=True, null=True)
  paid_capital = models.FloatField(default=0.0)
  paid_interests = models.FloatField(default=0.0)
  remaining_capital = models.FloatField(default=0.0)
  remaining_interests = models.FloatField(default=0.0)
  penalities_amount = models.FloatField(default=0.0)
  paid_amount = models.FloatField(default=0.0)
  remaining_amount = models.FloatField(default=0.0)
  total_amount = models.FloatField(default=0.0)
  status = models.CharField(max_length=255)
  
  
  def __str__(self):
    return f" credit of {self.holder}"