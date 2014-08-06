from django.db import models
from apps.sp.models.Country import Country
from django.utils.translation import ugettext_lazy as _


class Contract(models.Model):

    TYPE_PHOTO = 2
    TYPE_VIDEO = 1

    CHOICE_TYPE = (
        (TYPE_PHOTO,_(u'Foto')),
        (TYPE_VIDEO, _(u'Video'))
    )

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
        )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=TYPE_VIDEO
        )

    period_date = models.CharField(
        max_length=50,
        verbose_name=_(u'periodo de contrato (meses)'),
    )


    start_contract = models.DateField(
        verbose_name=_(u'Inicio del contrato'),
        null=False,
    )

    end_contract = models.DateField (
        verbose_name=_(u'Final del contrato'),
        null=False,
    )

    country = models.ManyToManyField(Country)

    type_contract =  models.ForeignKey(
        'TypeContract',
        verbose_name='tipo de contrato',
        related_name='contract_set',
        null=True
    )

    duration_month = models.IntegerField(
        editable=False,
        null=False,
        default=0
    )
    broadcast = models.ManyToManyField(
        'Broadcast',
        verbose_name='Medios',
        null=True
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


class TypeContract(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    name = models.CharField(
        max_length=45
    )
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    modified = models.DateTimeField(
        auto_now_add=True
    )
    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'