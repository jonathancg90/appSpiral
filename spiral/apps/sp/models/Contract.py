from django.db import models
from apps.sp.models.ModelHasCommercial import ModelHasCommercial
from django.utils.translation import ugettext_lazy as _


class Contract(models.Model):

    TYPE_PHOTO = 1
    TYPE_VIDEO = 0

    CHOICE_TYPE = (
        (TYPE_PHOTO,_(u'foto')),
        (TYPE_VIDEO, _(u'video'))
    )

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
        )

    status = models.SmallIntegerField(
        choices= CHOICE_STATUS
        )

    start_date = models.DateTimeField()

    ending_date = models.DateTimeField()

    created = models.DateTimeField(
    	auto_now_add=True,
        editable=False
        )
    modified = models.DateTimeField(
        auto_now_add=True
    )

    model_has_commercial = models.ForeignKey(
        ModelHasCommercial
    )

    type = models.SmallIntegerField(
        choices = CHOICE_TYPE
    )

    character = models.CharField(
        max_length=45
    )

    class Meta:
        app_label = 'sp'