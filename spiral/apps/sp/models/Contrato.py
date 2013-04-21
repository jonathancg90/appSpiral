from django.db import models
from apps.sp.models.Comercial import Comercial


class Contrato(models.Model):

    STATUS_ACTIVO = 1
    STATUS_INACTIVO = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVO,'inactivo'),
        (STATUS_ACTIVO, 'activo')
        )

    status = models.SmallIntegerField(
    	choices= CHOICE_STATUS
        )

    start_date = models.DateTimeField()

    ending_date = models.DateTimeField()

    created = models.DateTimeField(
    	auto_now_add=True
        )
    modified = models.DateTimeField()

    comercial_idcomercial = models.ForeignKey(Comercial)

    class Meta:
        app_label = 'sp'