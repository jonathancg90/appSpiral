from django.db import models
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):

    LINE_PHOTO = 4
    LINE_REPRESENTATION = 3
    LINE_EXTRA = 2
    LINE_CASTING = 1
    CHOICE_LINE = (
        (LINE_EXTRA, _(u'extra')),
        (LINE_CASTING, _(u'casting')),
        (LINE_REPRESENTATION, _(u'Representacion')),
        (LINE_PHOTO, _(u'Foto'))
    )

    STATUS_STAND_BY = 0
    STATUS_START = 1
    STATUS_FINISH = 2

    CHOICE_STATUS = (
        (STATUS_START, _(u'Iniciado')),
        (STATUS_FINISH, _(u'Terminado')),
        (STATUS_STAND_BY, _(u'Stand By'))
    )

    line_productions = models.SmallIntegerField(
        choices=CHOICE_LINE,
        default=LINE_CASTING
    )

    project_code = models.CharField(
        max_length=9,
        unique=True
    )

    commercial = models.ForeignKey(
        'Commercial',
        verbose_name='Comercial',
        related_name='project_set',
        null=True,
    )

    start_productions = models.DateField (
        verbose_name=_(u'Inicio de Produccion'),
        null=False,
    )

    end_productions = models.DateField (
        verbose_name=_(u'Final de Produccion'),
        null=False,
    )

    currency = models.ForeignKey(
        'Currency',
        verbose_name='Moneda',
        related_name='project_set'
    )

    budget = models.DecimalField(
        verbose_name=_(u'Presupuesto'),
        max_digits=10,
        decimal_places=2
    )

    budget_cost = models.DecimalField(
        verbose_name=_(u'Presupuesto de costo'),
        max_digits=10,
        decimal_places=2,
        null=True
    )

    observations = models.TextField(
        verbose_name='Observaciones'
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default= STATUS_START
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return self.project_code

    class Meta:
        app_label = 'sp'


class ProjectDetailStaff(models.Model):

    ROLE_PRODUCER = 1
    ROLE_EDITOR = 0
    ROLE_DIRECTOR = 2

    CHOICE_ROLE = (
        (ROLE_PRODUCER, 'Productor'),
        (ROLE_EDITOR, 'Editor'),
        (ROLE_DIRECTOR, 'Director')
    )

    project = models.ForeignKey(
        'Project',
        verbose_name='Proyecto',
        related_name='project_detail_set',
    )

    role = models.SmallIntegerField(
        choices=CHOICE_ROLE,
    )

    employee = models.SmallIntegerField()

    budget = models.DecimalField(
        verbose_name='Presupuesto de pago',
        max_digits=10,
        decimal_places=2,
        null=True
    )

    percentage = models.PositiveIntegerField(
        verbose_name='Porcentaje de ganancia',
        max_length= 3
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
