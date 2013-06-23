from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Brand(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
        )

    name = models.CharField(
        max_length = 45
        )
    entry = models.ForeignKey(
        'Entry',
        related_name='brand_set',
        )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
        )
    modified = models.DateTimeField(
        auto_now_add=True
    )

    status = models.SmallIntegerField(
        choices= CHOICE_STATUS,
        default = STATUS_ACTIVE
        )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'