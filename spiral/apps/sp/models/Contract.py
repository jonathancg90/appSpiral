from django.db import models
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

    start_date = models.DateTimeField(
        verbose_name=_(u'Inicio de contrato'),
    )

    ending_date = models.DateTimeField(
        verbose_name=_(u'Fin del contrato'),
    )

    type = models.SmallIntegerField(
        choices=CHOICE_TYPE,
        verbose_name=_(u'Tipo'),
    )

    character = models.CharField(
        max_length=45,
        verbose_name=_(u'Personaje'),
    )

    created = models.DateTimeField(
    	auto_now_add=True,
        editable=False
        )
    modified = models.DateTimeField(
        auto_now_add=True
    )

    model_has_commercial = models.ForeignKey(
        'ModelHasCommercial'
    )

    class Meta:
        app_label = 'sp'