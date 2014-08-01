from django.db import models


class Casting(models.Model):

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

    type_casting = models.ManyToManyField(
        'TypeCasting',
        verbose_name='Tipo de casting',
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


class CastingDetailModel(models.Model):

    CHARACTER_PRINCIPAL = 1
    CHARACTER_SECONDARY = 0
    CHOICE_CHARACTER = (
        (CHARACTER_PRINCIPAL, 'Principal'),
        (CHARACTER_SECONDARY, 'Secundario')
    )

    casting = models.ForeignKey(
        'Casting',
        related_name='casting_detail_model_set',
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

    type_casting = models.ManyToManyField(
        'TypeCasting',
        verbose_name='Tipo de casting',
        null=True
    )

    scene = models.CharField(
        verbose_name='Escena',
        max_length=100,
        null=True
    )

    budget = models.DecimalField(
        verbose_name='Presupuesto',
        max_digits=10,
        decimal_places=2,
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
        return '%s %s' %(self.quantity, self.profile)

    class Meta:
        app_label = 'sp'
