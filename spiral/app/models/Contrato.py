from django.db import models
from app.models.Comercial import Comercial


class Contratos(models.Model):

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

    comercial_idcomercial = models.ForeingKey(Comercial)

