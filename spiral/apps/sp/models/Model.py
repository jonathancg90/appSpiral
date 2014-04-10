from django.utils.translation import ugettext_lazy as _
from django.utils import simplejson
from django.db import models
import urllib2
import random


class Model(models.Model):

    STATUS_WEBSITE = 3 #Registrado a traves de la web
    STATUS_DISAPPROVE = 2 #Modelo betado
    STATUS_ACTIVE = 1 #Modelo registrado en spiral(acepto las condiciones)
    STATUS_INACTIVE = 0

    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'Inactivo')),
        (STATUS_ACTIVE, _(u'Activo')),
        (STATUS_DISAPPROVE, _(u'Sin aprobar'))
    )

    GENDER_MASC = 1
    GENDER_FEM = 2

    GENDER_CHOICES = (
        (GENDER_MASC, _(u'Masculino')),
        (GENDER_FEM, _(u'Femenino'))
    )

    TYPE_DNI = 1
    TYPE_CARNET = 2
    TYPE_PASSPORT = 3

    TYPE_DOCUMENTS = (
        (TYPE_CARNET, 'Carnet de extrangeria'),
        (TYPE_DNI, 'DNI'),
        (TYPE_PASSPORT, 'Pasaport')
    )

    model_code = models.CharField(
        verbose_name=_('Codigo'),
        max_length=45,
        unique=True
    )

    type_doc = models.SmallIntegerField(
        choices=TYPE_DOCUMENTS,
        default=TYPE_DNI
    )

    number_doc = models.CharField(
        verbose_name=_('Numero de documento'),
        max_length=15,
        null=True
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

    birth = models.DateField(
        verbose_name=_(u'Fecha Nacimiento'),
        null=False
    )

    gender = models.SmallIntegerField(
        choices=GENDER_CHOICES,
        default=GENDER_MASC
    )

    address = models.CharField(
        verbose_name=_('Direccion'),
        max_length=100,
        null=True,
    )

    email = models.EmailField(
        max_length=100,
        null=True
    )

    nationality = models.ForeignKey(
        'country',
        verbose_name=_(u'Nacionalidad'),
        related_name='model_set',
        null=True,
    )

    phone_fixed = models.CharField(
        verbose_name=_(u'Telefono fijo'),
        max_length=20,
        null=True,
        blank=True,
    )

    phone_mobil = models.CharField(
        verbose_name=_(u'Telefono mobil'),
        max_length=20,
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

    @classmethod
    def get_types(self):
        choices = []
        for type in Model.TYPE_DOCUMENTS:
            choices.append({
                'id': type[0],
                'name': type[1]
            })
        return choices

    @classmethod
    def get_code(self):
        return random.randint(200, 500)

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
                    'dni':api.get('dni'),
                    'telefonos':api.get('telefonos'),
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


class ModelFeatureDetail(models.Model):
    model = models.ForeignKey(
        'Model',
        related_name='model_feature_detail_set',
    )

    feature_value = models.ForeignKey(
        'FeatureValue',
        related_name='model_feature_detail_set',
    )

    description = models.CharField(
        verbose_name=_(u'Descripcion'),
        max_length=100,
        null=True,
        blank=True
    )

    class Meta:
        app_label = 'sp'