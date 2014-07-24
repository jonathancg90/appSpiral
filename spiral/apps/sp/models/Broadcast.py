from django.db import models


class Broadcast(models.Model):

    STATUS_ACTIVE = 1
    STATUS_DELETE = 2
    STATUS_INACTIVE = 3
    CHOICE_STATUS = (
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_INACTIVE, 'Inactivo'),
        (STATUS_DELETE, 'Eliminado')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=70
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'