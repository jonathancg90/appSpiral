from django.db import models


class Modelos_has_contratos(models.Model):
	
	created = models.DateTimeField(
		auto_now_add=True
		)
	modified = models.DateTimeField()