from django.db import models
from django.utils.translation import ugettext_lazy as _
from apps.sp.models.Model import Model
from apps.sp.models.Commercial import Commercial


class ModelHasCommercial(models.Model):

    model = models.ForeignKey(
        Model
    )

    commercial = models.ForeignKey(
        Commercial
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