from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class List(models.Model):
    STATUS_ACTIVE = 1
    STATUS_ARCHIVE = 0
    CHOICE_STATUS = (
        (STATUS_ARCHIVE, _(u'archivado')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    title = models.CharField(
        max_length=45,
        verbose_name='Titulo'
    )

    description = models.CharField(
        max_length=200,
        verbose_name='descripcion'
    )

    project = models.ForeignKey(
        'Project',
        related_name='list_set',
        null=True
    )

    collaboration = models.ManyToManyField(
        User,
        through='UserCollaborationDetail'
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
        return self.date

    class Meta:
        app_label = 'sp'



class UserCollaborationDetail(models.Model):

    user = models.ForeignKey(User)
    list = models.ForeignKey(List)
    is_owner = models.BooleanField(
        default=False
    )

    class Meta:
        app_label = 'sp'

    @property
    def user_owner(self):
        user_collaboration = UserCollaborationDetail.objects.get(
            list=self.list,
            is_owner=True
        )
        return user_collaboration.user


class DetailList(models.Model):

    list = models.ForeignKey(List)

    available = models.BooleanField(
        default=True
    )

    model = models.ForeignKey(
        'Model',
        related_name='detail_list_set',
        null=True
    )

    name_complete = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        null=True
    )

    DNI = models.CharField(
        max_length=8,
        verbose_name='DNI',
        null=True
    )

    phone = models.CharField(
        max_length=100,
        verbose_name='Telefonos',
        null=True
    )

    observation = models.CharField(
        max_length=200,
        verbose_name='Observaciones',
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

    class Meta:
        app_label = 'sp'


