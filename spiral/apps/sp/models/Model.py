import urllib2
import json

from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.utils import simplejson
from django.db import models
from apps.sp.models.Feature import FeatureValue


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
        (GENDER_MASC, 'Masculino'),
        (GENDER_FEM, 'Femenino')
    )

    TYPE_DNI = 1
    TYPE_CARNET = 2
    TYPE_PASSPORT = 3
    TYPE_FAKE = 4

    TYPE_DOCUMENTS = (
        (TYPE_CARNET, 'Carnet de extranjeria'),
        (TYPE_DNI, 'DNI'),
        (TYPE_PASSPORT, 'Pasaporte')
    )
    model_code = models.PositiveIntegerField(
        unique=True
    )

    type_doc = models.SmallIntegerField(
        choices=TYPE_DOCUMENTS,
        default=TYPE_DNI
    )

    number_doc = models.CharField(
        verbose_name=_('Numero de documento'),
        max_length=15,
        null=True,
        unique=True
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    name_complete = models.CharField(
        verbose_name=_('Nombre completo'),
        max_length=65
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

    city = models.ForeignKey(
        'city',
        verbose_name=_(u'ciudad'),
        related_name='model_set',
        null=True,
    )

    phone_fixed = models.CharField(
        verbose_name=_(u'Telefono fijo'),
        max_length=40,
        null=True,
        blank=True,
    )

    phone_mobil = models.CharField(
        verbose_name=_(u'Telefono mobil'),
        max_length=40,
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

    main_image = models.CharField(
        verbose_name=_(u'Imagen Principal'),
        max_length=100,
        default='img/default.png',
        null=True,
        blank=True,
    )

    summary = models.TextField(
        verbose_name=_(u'Resumen'),
        null=True,
        blank=True,
    )

    terms = models.BooleanField(
        verbose_name=_(u'Terminos y condiciones'),
        default=False,
    )

    feature_detail = models.ManyToManyField(
        FeatureValue,
        through='ModelFeatureDetail'
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
        return self.name_complete

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
    def get_genders(self):
        choices = []
        for gender in Model.GENDER_CHOICES:
            choices.append({
                'id': gender[0],
                'name': gender[1]
            })
        return choices

    @classmethod
    def get_code(self):
        initial = 100000
        try:
            model = Model.objects.latest('model_code')
            if model:
                return model.model_code + 1
            else:
                return initial
        except Model.DoesNotExist:
            return initial

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


def create_additional_data(sender, instance, created, **kwargs):
    if instance.model_code is None:
        instance.model_code = Model.get_code()
    post_save.disconnect(create_additional_data, sender=Model) #for not causing recursion
    instance.save()
    post_save.connect(create_additional_data, sender=Model)

post_save.connect(create_additional_data, sender=Model)


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
        max_length=150,
        null=True,
        blank=True
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

    def __unicode__(self):
        return self.feature_value.name


def update_model_summary(sender, instance, created, **kwargs):
    data = {}
    model = instance.model
    features = model.model_feature_detail_set.all()
    features = features.select_related('feature_value')
    for feature_detail in features:
        data.update({
            feature_detail.feature_value_id : feature_detail.description
        })
    model.summary = json.dumps(data)
    model.save()
    post_save.connect(create_additional_data, sender=Model)

post_save.connect(update_model_summary, sender=ModelFeatureDetail)