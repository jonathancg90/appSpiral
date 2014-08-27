from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Pauta(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'')),
        (STATUS_ACTIVE, _(u'activo'))
    )
    project = models.ForeignKey(
        'Entry',
        related_name='brand_set',
    )
    date = models.DateField(
        verbose_name='Fecha de pauta',
    )
    users = models.ManyToManyField(
        User
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    modified = models.DateTimeField(
        editable=False,
        auto_now=True
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    def __unicode__(self):
        return self.date

    class Meta:
        app_label = 'sp'


class DetailPauta(models.Model):
    STATUS_PENDING = 1
    STATUS_ASSIST= 0
    STATUS_CANCELED = 0
    CHOICE_STATUS = (
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_ASSIST, 'Asistio'),
        (STATUS_CANCELED, 'Cancelado')
    )

    hour = models.TimeField(
        verbose_name='Hora',
        null=True,
    )

    model = models.ForeignKey(
        'Model',
        related_name='detail_pauta_set',
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        null=True
    )

    character = models.SmallIntegerField(
        default=0
    )

    observation = models.CharField(
        max_length=200,
        verbose_name='Observaciones',
        null=True
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_PENDING
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        editable=False,
        auto_now=True
    )

