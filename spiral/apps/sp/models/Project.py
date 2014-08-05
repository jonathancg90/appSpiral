from django.db import models
from apps.sp.models.Client import Client, TypeClient
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):

    LINE_PHOTO = 4
    LINE_REPRESENTATION = 3
    LINE_EXTRA = 2
    LINE_CASTING = 1
    CHOICE_LINE = (
        (LINE_EXTRA, 'extra'),
        (LINE_CASTING, 'casting'),
        (LINE_REPRESENTATION, 'Representacion'),
        (LINE_PHOTO, 'Foto')
    )

    STATUS_STAND_BY = 0
    STATUS_START = 1
    STATUS_FINISH = 2
    STATUS_EXTEND = 3
    STATUS_DELETE = 4

    CHOICE_STATUS = (
        (STATUS_START, _(u'Iniciado')),
        (STATUS_FINISH, _(u'Terminado')),
        (STATUS_STAND_BY, _(u'Stand By')),
        (STATUS_EXTEND, _(u'Extendido')),
        (STATUS_DELETE, _(u'Eliminado'))
    )

    line_productions = models.SmallIntegerField(
        choices=CHOICE_LINE,
        default=LINE_CASTING
    )

    code = models.IntegerField(
        editable=False,
        null=False,
        default=1
    )
    version = models.IntegerField(
        editable=False,
        null=False,
        default=0
    )

    commercial = models.ForeignKey(
        'Commercial',
        verbose_name='Comercial',
        related_name='project_set',
        null=True,
    )

    client = models.ManyToManyField(
        Client,
        through='ProjectClientDetail'
    )

    start_productions = models.DateField(
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
        related_name='project_set',
        null=True
    )

    budget = models.DecimalField(
        verbose_name=_(u'Presupuesto'),
        max_digits=10,
        decimal_places=2,
        default=0
    )

    budget_cost = models.DecimalField(
        verbose_name=_(u'Presupuesto de costo'),
        max_digits=10,
        decimal_places=2,
        null=True
    )

    observations = models.TextField(
        verbose_name='Observaciones',
        null=True
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
        try:
            return self.commercial.name
        except:
            return ''

    class Meta:
        app_label = 'sp'

    def get_code(self):
        code = ''
        number = str(self.code)
        date = self.start_productions
        moth = str(date.month)
        year = str(date.year)
        if self.line_productions == self.LINE_CASTING:
            line = 'M'

        if self.line_productions == self.LINE_EXTRA:
            line = 'E'

        if self.line_productions == self.LINE_PHOTO:
            line = 'F'

        if self.line_productions == self.LINE_REPRESENTATION:
            line = 'R'

        if len(number) == 1:
            number = '0' + number
        if len(moth) == 1:
            moth = '0' + moth

        code = year[2:4] + '-' + moth + line + number + str(self.version)

        return code


class DutyDetail(models.Model):
    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    type_contract =  models.ForeignKey(
        'TypeContract',
        verbose_name='tipo de contrato',
        related_name='duty_detail_set',
        null=True
    )
    duration_month = models.IntegerField(
        editable=False,
        null=False,
        default=0
    )
    broadcast = models.ManyToManyField(
        'Broadcast',
        verbose_name='Medios',
        null=True
    )
    country = models.ManyToManyField(
        'Country',
        verbose_name='Paises',
        null=True
    )

    class Meta:
        app_label = 'sp'


class ProjectClientDetail(models.Model):
    project = models.ForeignKey(Project)
    client = models.ForeignKey(Client)
    type = models.ForeignKey(TypeClient)

    class Meta:
        app_label = 'sp'


class ProjectDetailDeliveries(models.Model):
    project = models.ForeignKey(
        'Project',
        verbose_name='Proyecto',
        related_name='project_detail_deliveries_set',
        null=True
    )

    delivery_date = models.DateField(
        verbose_name=_(u'Fecha de entrega'),
        null=False,
    )

    class Meta:
        app_label = 'sp'


class ProjectDetailStudio(models.Model):

    project = models.ForeignKey(
        'Project',
        verbose_name='Proyecto',
        related_name='project_detail_studio_set',
        null=True
    )

    studio = models.ForeignKey(
        'Studio',
        verbose_name='Estudio',
        related_name='project_detail_studio_set',
        null=True
    )

    class Meta:
        app_label = 'sp'


class ProjectDetailStaff(models.Model):

    ROLE_PRODUCER = 1
    ROLE_EDITOR = 0
    ROLE_DIRECTOR = 2

    CHOICE_ROLES = (
        (ROLE_PRODUCER, 'Productor'),
        (ROLE_EDITOR, 'Editor'),
        (ROLE_DIRECTOR, 'Director')
    )

    project = models.ForeignKey(
        'Project',
        verbose_name='Proyecto',
        related_name='project_detail_staff_set',
        null=True
    )

    role = models.SmallIntegerField(
        choices=CHOICE_ROLES,
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
        verbose_name='Observaciones',
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
