from django.db import models

class Model(models.Model):

    model_code = models.CharField(
        max_length=45
    )
    created = models.DateTimeField(
    	auto_now_add=True,
        editable=False
        )
    modified = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        app_label = 'sp'