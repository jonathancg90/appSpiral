from django.db import models

# Create your models here.


class Rubro(models.Model):

	STATUS_ACTIVO = 1
	STATUS_INACTIVO = 0
	CHOICE_STATUS = (
		(STATUS_INACTIVO,'inactivo'),
		(STATUS_ACTIVO, 'activo')
		)

	nombre = models.CharField(
		max_lenght=45
		)
	created = models.DateTimeField(
		auto_now_add=True
		)
	modified = models.DateTimeField()
	status = models.SmallIntegerField(
		choices= CHOICE_STATUS
		) 
