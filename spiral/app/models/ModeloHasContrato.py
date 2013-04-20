from django.db import models


class ModelosHasContratos(models.Model):
	
	created = models.DateTimeField(
		auto_now_add=True
		)
	modified = models.DateTimeField()