from django.db import models


class Representation(models.Model):

    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    ppi = models.DateField(
        verbose_name='PPI',
        null=True,
    )

    ppg = models.DateField(
        verbose_name='PPG',
        null=True,
    )

    type_event = models.ForeignKey(
        'TypeEvent',
        verbose_name='Tipo de evento',
        related_name='representation_set',
        null=True
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

    representation = models.ForeignKey(
        'Representation',
        verbose_name='Modelo',
        related_name='representation_detail_model_set',
    )

    profile = models.CharField(
        verbose_name='Perfil',
        max_length=100,
        null=True,
    )

    model = models.ForeignKey(
        'Model',
        null=True,
        verbose_name='Modelo',
        related_name='representation_detail_model_set',
    )

    character = models.SmallIntegerField(
        choices=CHOICE_CHARACTER,
        default=CHARACTER_PRINCIPAL
    )

    currency = models.ForeignKey(
        'Currency',
        verbose_name='Moneda',
        related_name='representation_detail_model_set',
        null=True
    )

    budget = models.DecimalField(
        verbose_name='Presupuesto',
        max_digits=10,
        decimal_places=2,
        null=True
    )

    budget_cost = models.DecimalField(
        verbose_name='Presupuesto para el modelo',
        max_digits=10,
        decimal_places=2,
        null=True
    )

    schedule = models.TextField(
        verbose_name='Horario',
        null=True
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
