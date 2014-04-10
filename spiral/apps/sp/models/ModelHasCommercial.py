from django.db import models


class ModelHasCommercial(models.Model):

    model = models.ForeignKey(
        'Model',
        related_name='model_has_commercial_set'
    )

    commercial = models.ForeignKey(
        'Commercial',
        related_name='model_has_commercial_set'
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