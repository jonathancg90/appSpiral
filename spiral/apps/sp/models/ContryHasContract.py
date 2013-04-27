from apps.sp.models.Country import Country
from apps.sp.models.Contract import Contract
from django.db import models

class CountryHasContract(models.Model):
    country_id = models.ForeignKey(
        Country
    )
    contract_id =models.ForeignKey(
        Contract
    )
