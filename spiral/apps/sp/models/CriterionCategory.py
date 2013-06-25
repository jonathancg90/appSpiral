from django.db import models
from django.utils.translation import ugettext_lazy as _


class CriterionCategory(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )
    description = models.CharField(
        max_length=45
    )
    status = models.SmallIntegerField(
        choices= CHOICE_STATUS,
        default=STATUS_ACTIVE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    modified = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return self.description

    class Meta:
        app_label = 'sp'