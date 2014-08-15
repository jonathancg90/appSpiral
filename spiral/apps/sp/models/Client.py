from django.db import models


class TypeClient(models.Model):

    name = models.CharField(
        max_length=60,
        verbose_name='Tipo de Cliente',
        )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'


class Client(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    STATUS_ABROAD = 2
    CHOICE_STATUS = (
        (STATUS_INACTIVE, 'inactivo'),
        (STATUS_ACTIVE, 'activo'),
        (STATUS_ACTIVE, 'extranjero')
    )

    name = models.CharField(
        max_length=60,
        verbose_name='Razon Social',
    )

    ruc = models.CharField(
        max_length=11,
        verbose_name='R.U.C',
        unique=True
    )

    address = models.CharField(
        max_length=70,
        verbose_name='Direccion',
        null=True
    )

    type_client = models.ManyToManyField(TypeClient)

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        editable=False,
        auto_now=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'

