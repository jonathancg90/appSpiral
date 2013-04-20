from django.db import models
from app.models.Marca import Marcas
from app.models.ModeloHasContrato import ModelosHasContratos


class Comercial(models.Model):
		
	STATUS_ACTIVO = 1
	STATUS_INACTIVO = 0
	CHOICE_STATUS = (
		(STATUS_INACTIVO,'inactivo'),
		(STATUS_ACTIVO, 'activo')
		)

	nombre = models.CharField(
		max_lenght=50
		)
	realizado = models.DateTimeField()
	
	marcas_idmarcas = models.ForeingKey(
		Marcas
		)
	status = models.SmallIntegerField(
		choices= CHOICE_STATUS
		) 

	modelo_has_contratos = models.ForeingKey(ModelosHasContratos)