from django.utils.translation import ugettext_lazy as _
from django.db import models
from apps.sp.models.Marca import Marca
from apps.sp.models.ModeloHasContrato import ModeloHasContrato


class Comercial(models.Model):

    STATUS_ACTIVO = 1
    STATUS_INACTIVO = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVO,_(u'inactivo')),
        (STATUS_ACTIVO, _(u'activo'))
    )

    nombre = models.CharField(
        verbose_name=_(u'Nombre'),
        max_length = 50
	    )
    realizado = models.DateTimeField()
	
    marcas_idmarcas = models.ForeignKey(
	    Marca
	    )
    status = models.SmallIntegerField(
	    choices= CHOICE_STATUS
        )

    modelo_has_contratos = models.ForeignKey(ModeloHasContrato)

    class Meta:
        app_label = 'sp'