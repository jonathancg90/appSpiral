from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class Pauta(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'')),
        (STATUS_ACTIVE, _(u'activo'))
    )
    project = models.ForeignKey(
        'Project',
        related_name='pauta_set',
    )

    date = models.DateField(
        verbose_name='Fecha de pauta',
    )

    users = models.ManyToManyField(
        User
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
        return self.project

    class Meta:
        app_label = 'sp'


class DetailPauta(models.Model):
    STATUS_PENDING = 1
    STATUS_ASSIST= 2
    STATUS_CANCELED = 0
    STATUS_ABSENCE = 3
    STATUS_RETIRE = 4
    CHOICE_STATUS = (
        (STATUS_PENDING, 'Pendiente'),
        (STATUS_ASSIST, 'Asistio'),
        (STATUS_CANCELED, 'Cancelado'),
        (STATUS_ABSENCE, 'Falto'),
        (STATUS_RETIRE, 'Se retiro')
    )

    pauta = models.ForeignKey(
        'Pauta',
        related_name='detail_pauta_set',
    )

    hour = models.TimeField(
        verbose_name='Hora',
    )

    model = models.ForeignKey(
        'Model',
        related_name='detail_pauta_set',
        null=True
    )

    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        null=True
    )

    character = models.SmallIntegerField(
        default=0
    )

    observation = models.CharField(
        max_length=200,
        verbose_name='Observaciones',
        null=True
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_PENDING
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        editable=False,
        auto_now=True
    )

    class Meta:
        app_label = 'sp'

    @property
    def character_display(self):
        project = self.pauta.project
        project.line_productions
        project.get_line_productions_display()


        self.character
        return user_collaboration.user

