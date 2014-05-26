from apps.sp.models.Country import Country
from apps.sp.models.Contract import Contract
from django.db import models

class CountryHasContract(models.Model):
    country = models.ForeignKey(
        Country
    )
    contract =models.ForeignKey(
        Contract
    )
    class Meta:
        app_label = 'sp'