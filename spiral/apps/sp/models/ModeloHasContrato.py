from django.db import models


class ModeloHasContrato(models.Model):
	
    created = models.DateTimeField(
    	auto_now_add=True
    	)
    modified = models.DateTimeField()

    class Meta:
        app_label = 'sp'