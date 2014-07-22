from django.db import models


class Extras(models.Model):

    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    class Meta:
        app_label = 'sp'


class ExtrasDetailModel(models.Model):

    CHARACTER_PRINCIPAL = 1
    CHARACTER_SECONDARY = 0
    CHOICE_CHARACTER = (
        (CHARACTER_PRINCIPAL, 'Extra'),
        (CHARACTER_SECONDARY, 'Extra especial')
    )

    extras = models.ForeignKey(
        'Extras',
        related_name='extras_detail_model_set',
    )

    quantity = models.SmallIntegerField()

    profile = models.CharField(
        verbose_name='Perfil',
        max_length=100
    )

    feature = models.CharField(
        verbose_name='Carracteristicas',
        max_length=200,
        null=True
    )

    character = models.SmallIntegerField(
        choices=CHOICE_CHARACTER,
        default=CHARACTER_PRINCIPAL,
        null=True
    )

    currency = models.ForeignKey(
        'Currency',
        verbose_name='Moneda',
        related_name='extra_detail_set',
        null=True
    )

    budget = models.DecimalField(
        verbose_name='Presupuesto',
        max_digits=10,
        decimal_places=2
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
        auto_now_add=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'