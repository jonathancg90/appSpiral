from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.


class Rubro(models.Model):

    STATUS_ACTIVO = 1
    STATUS_INACTIVO = 0
    CHOICE_STATUS = (
	    (STATUS_INACTIVO,_(u'inactivo')),
	    (STATUS_ACTIVO, _(u'activo'))
	    )

    nombre = models.CharField(
        max_length = 45
	    )
    created = models.DateTimeField(
		auto_now_add=True
	    )
    modified = models.DateTimeField()
    status = models.SmallIntegerField(
        choices= CHOICE_STATUS
        )

    def __unicode__(self):
        return self.nombre

    class Meta:
        app_label = 'sp'