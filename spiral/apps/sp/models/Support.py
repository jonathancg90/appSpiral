from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Support(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    text = models.TextField()

    user = models.ForeignKey(User)

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
        return self.text

    class Meta:
        app_label = 'sp'