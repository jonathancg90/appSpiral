from django.db import models


class Casting(models.Model):

    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    ppi = models.DateField (
        verbose_name='PPI',
        null=True,
    )

    ppg = models.DateField (
        verbose_name='PPG',
        null=True,
    )

    type_casting = models.ForeignKey(
        'TypeCasting',
        verbose_name='Tipo de casting',
        related_name='casting_set',
    )

    class Meta:
        app_label = 'sp'


class TypeCasting(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, 'inactivo'),
        (STATUS_ACTIVE, 'activo')
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
