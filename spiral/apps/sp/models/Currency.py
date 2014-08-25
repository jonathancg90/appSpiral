from django.db import models


class Currency(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, 'inactivo'),
        (STATUS_ACTIVE, 'activo')
    )
    symbol = models.CharField(
        verbose_name='Simbolo',
        max_length=5
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=45
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
        return self.name

    class Meta:
        app_label = 'sp'