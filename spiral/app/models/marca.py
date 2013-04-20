from django.db import models
from app.models.rubro import Rubro

# Create your models here.

class Marcas(models.Model):}
	STATUS_ACTIVO = 1
	STATUS_INACTIVO = 0
	CHOICE_STATUS = (
		(STATUS_INACTIVO,'inactivo'),
		(STATUS_ACTIVO, 'activo')
		)

	nombre = models.CharField(
		max_lenght=45
		)
	rubro_idrubro = models.ForeingKey(
		Rubro
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