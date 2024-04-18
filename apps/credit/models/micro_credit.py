from django.utils import timezone
from django.db import models
from apps.authentication.models import User
import datetime


class MicroCredit(models.Model):
    STATUS_CHOICES = [
        ('INITIAL', 'Initial'),
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    ]

    # Define model fields
    amount = models.FloatField()
    holder = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    created_at = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_microcredit'
    )
    approved_at = models.DateField(blank=True, null=True)
    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='approved_microcredit'
    )
    cancelled_at = models.DateField(blank=True, null=True)
    cancelled_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='cancelled_microcredit'
    )
    rejected_at = models.DateField(blank=True, null=True)
    rejected_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='rejected_microcredit'
    )
    credit_type = models.ForeignKey(
        "MicroCreditType",
        on_delete=models.SET_NULL,
        null=True
    )
    period = models.ForeignKey(
        "Period",
        on_delete=models.SET_NULL,
        null=True
    )
    payment_date = models.DateField(
        blank=True,
        null=True
    )
    expiration_date = models.DateField(
        blank=True,
        null=True
    )
    delay_days = models.IntegerField(
        blank=True,
        null=True
    )
    interest_rate = models.FloatField(
        blank=True,
        null=True
    )
    penalties_rate = models.FloatField(
        blank=True,
        null=True
    )
    paid_capital = models.FloatField(
        default=0.0
    )
    paid_interests = models.FloatField(
        default=0.0
    )
    remaining_capital = models.FloatField(
        default=0.0
    )
    remaining_interests = models.FloatField(
        default=0.0
    )
    penalties_amount = models.FloatField(
        default=0.0
    )
    paid_amount = models.FloatField(
        default=0.0
    )
    remaining_amount = models.FloatField(
        default=0.0
    )
    total_amount = models.FloatField(
        default=0.0
    )
    interest_amount = models.FloatField(
        default=0.0
    )  # New field for interest amount
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='INITIAL'
    )



    # Update credit status and financial details
    def pay_credit(self):
        if self.status == 'PENDING':
            self.status = 'PAID'
            self.paid_amount = self.total_amount
            self.remaining_amount = 0.0
            self.paid_capital = self.amount
            self.paid_interests = self.interest_amount
            self.remaining_capital = 0.0
            self.remaining_interests = 0.0
            self.save()
        elif self.status == 'INITIAL':
            raise ValueError('Cannot pay the credit with the initial status')
        elif self.status == 'REJECTED':
            raise ValueError('Cannot pay the credit with the rejected status')
        elif self.status == 'CANCELLED':
            raise ValueError('Cannot pay the credit with the cancelled status')
        elif self.status == 'PAID':
            raise ValueError('This credit has already been paid')
        else:
            raise ValueError('Cannot pay this credit, please contact the admin for more information')



    def approve_credit(self):
        # Update credit status to approved and add time
        if self.status == 'INITIAL':

            self.status = 'PENDING'
            self.approved_at = timezone.now()
            self.save()
        else:
            raise ValueError('The credit must have the initial status to be approved')

    def reject_credit(self):
        # Update credit status to rejected and add time
        if self.status == 'INITIAL':
            self.status = 'REJECTED'
            self.rejected_at = timezone.now()
            self.save()
        else:
            raise ValueError('The credit must have the initial status to be rejected')

    def cancel_credit(self):
        # Update credit status to cancelled and add time
        if self.status == 'PENDING':
            self.status = 'CANCELLED'
            self.cancelled_at = timezone.now()
            self.save()
        else:
            raise ValueError('The credit must have the pending status to be cancelled')


    # Override save method to handle calculations and validations
    def save(self, *args, **kwargs):

        if self.amount and self.interest_rate:
            # Calculate interest
            self.interest_amount = self.amount * (self.interest_rate / 100)

            rest_interest = self.interest_amount - self.paid_interests

            self.remaining_interests = rest_interest

        if self.amount and self.penalties_rate:
            # Calculate penalties
            self.penalties_amount = self.amount * (self.penalties_rate / 100)
        # Calculate total amount
        plus_amount = self.remaining_interests + self.penalties_amount
        self.total_amount = self.amount + plus_amount
        # Calculate remaining amount
        self.remaining_amount = self.total_amount - self.paid_amount

        # Calculate remaining capital whenever paid capital changes
        if self.paid_capital is not None:
            self.remaining_capital = self.amount - self.paid_capital

        if self.expiration_date:
            # Convert expiration_date to a datetime object for comparison
            expiration_datetime = datetime.datetime.combine(self.expiration_date, datetime.time.min)
            expiration_datetime = timezone.make_aware(expiration_datetime, timezone.get_current_timezone())


            if expiration_datetime >= timezone.now():
                # Check if penalties_rate is not None before using it
                if self.penalties_rate is not None:
                    self.penalties_amount = self.amount * (self.penalties_rate / 100)

                else:
                    self.penalties_amount = 0.0
            else:
                self.penalties_amount = 0.0
        else:
            self.penalties_amount = 0.0


        super().save(*args, **kwargs)
