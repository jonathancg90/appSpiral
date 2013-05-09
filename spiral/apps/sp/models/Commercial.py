from django.utils.translation import ugettext_lazy as _
from django.db import models


class Commercial(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    name = models.CharField(
        verbose_name=_(u'Nombre'),
        max_length=50
    )
    realized = models.DateTimeField(
        verbose_name=_(u'Realizado'),
    )

    brand = models.ForeignKey(
        'Brand',
        verbose_name=_(u'Marca'),
        related_name='commercial_set',
    )
    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
        )

    project = models.ForeignKey(
        'Project',
        related_name='commercial_set',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'