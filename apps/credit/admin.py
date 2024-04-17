from django.contrib import admin
from .models.micro_credit_type import MicroCreditType
from .models.micro_credit import MicroCredit
from .models.period import Period



sites=(MicroCredit, MicroCreditType, Period)

admin.site.register(sites)



