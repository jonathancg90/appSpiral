from django.utils.translation import ugettext_lazy as _
from django.db import models
import urllib2
import simplejson


class Model(models.Model):

    STATUS_DISAPPROVE = 3
    STATUS_EXCLUSIVE = 2
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'Inactivo')),
        (STATUS_ACTIVE, _(u'Activo')),
        (STATUS_EXCLUSIVE, _(u'Exclusivo')),
        (STATUS_DISAPPROVE, _(u'Sin aprobar'))
    )

    model_code = models.CharField(
        verbose_name=_('Codigo'),
        max_length=45,
        unique=True
    )

    dni = models.CharField(
        verbose_name=_('DNI'),
        max_length=15,
        null=True,
        unique=True
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    name = models.CharField(
        verbose_name=_('Nombres'),
        max_length=45
    )

    last_name = models.CharField(
        verbose_name=_('Apellidos'),
        max_length=45
    )

    alias = models.CharField(
        max_length=45,
        null=True,
        blank=True,
    )

    address = models.CharField(
        verbose_name=_('Direccion'),
        max_length=100,
        null=True,
    )

    reference = models.CharField(
        verbose_name=_('Referencia'),
        max_length=100,
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=100,
        null=True
    )

    birth = models.DateField(
        verbose_name=_(u'Fecha Nacimiento'),
        null=False
    )

    birth_place = models.CharField(
        verbose_name=_(u'Lugar de nacimiento'),
        max_length=100,
        null=True,
        blank=True,
    )

    height = models.DecimalField(
        verbose_name=_(u'Altura'),
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True,
    )

    weight = models.DecimalField(
        verbose_name=_(u'Peso'),
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
    )

    size_shoe = models.DecimalField(
        verbose_name=_(u'Talla Zapato'),
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )

    experience = models.CharField(
        verbose_name=_(u'Experiencia'),
        max_length=300,
        default=_(u'Ninguna')
    )

    last_visit = models.DateField(
        verbose_name=_(u'Ultima visita'),
        null=True,
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return '%s %s' % (self.name, self.last_name)

    class Meta:
        app_label = 'sp'

    def get_data_api_json(self):
        if self.model_code is not None:
            try:
                url = 'http://192.168.1.3/sistemas/proyspiral/api/model.php?codigo='+self.model_code
                req = urllib2.Request(url, None, {'user-agent':'syncstream/vimeo'})
                opener = urllib2.build_opener()
                f = opener.open(req,timeout=1)
                api = simplejson.load(f)
                data = {
                    'modelo':api.get('modelo'),
                    'estatura':api.get('estatura'),
                    'edad':api.get('edad'),
                    'response': True
                }
                return data
            except:
                pass

        data = {
            'modelo':self.model_code,
            'response': False
        }
        return data


class ModelPhone(models.Model):

    LANDLINE = 4
    OPERATOR_CLARO = 3
    OPERATOR_MOVISTAR = 2
    OPERATOR_NEXTEL = 1
    CHOICE_OPERATOR = (
        (LANDLINE, _(u'Telefono fijo')),
        (OPERATOR_CLARO, _(u'Claro')),
        (OPERATOR_MOVISTAR, _(u'Movistar')),
        (OPERATOR_NEXTEL, _(u'Nextel'))
    )

    model = models.ForeignKey(
        'Model',
        verbose_name=_(u'Modelo'),
        related_name='model_phone_set',
    )

    type = models.SmallIntegerField(
        choices=CHOICE_OPERATOR,
        default=LANDLINE
    )

    number = models.CharField(
        verbose_name=_(u'Numero telefonico'),
        max_length=10,
    )

    class Meta:
        app_label = 'sp'