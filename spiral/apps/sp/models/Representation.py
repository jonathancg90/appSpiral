from django.db import models


class Representation(models.Model):

    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    photo_use = models.CharField(
        verbose_name='Uso de la foto',
        null=True,
        max_length=200
    )

    type_event = models.ForeignKey(
        'TypeEvent',
        verbose_name='Tipo de evento',
        related_name='representation_set',
    )

    class Meta:
        app_label = 'sp'


class TypeEvent(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, 'inactivo'),
        (STATUS_ACTIVE, 'activo')
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


class RepresentationDetailModel(models.Model):

    CHARACTER_EXTRA = 1
    CHARACTER_SPECIAL_EXTRA = 0
    CHARACTER_PRINCIPAL = 2
    CHARACTER_AMPHITRYON = 3
    CHARACTER_BOOSTER = 4

    CHOICE_CHARACTER = (
        (CHARACTER_EXTRA, 'Extra'),
        (CHARACTER_SPECIAL_EXTRA, 'Extra Especial'),
        (CHARACTER_PRINCIPAL, 'Modelo Principal'),
        (CHARACTER_AMPHITRYON, 'Anfitrion'),
        (CHARACTER_BOOSTER, 'Impulsadora')
    )

    profile = models.CharField(
        verbose_name='Perfil',
        max_length=100
    )

    model = models.ForeignKey(
        'Model',
        verbose_name='Modelo',
        related_name='representation_set',
    )

    character = models.SmallIntegerField(
        choices=CHOICE_CHARACTER,
        default=CHARACTER_PRINCIPAL
    )

    observations = models.TextField(
        verbose_name='Observaciones'
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'
