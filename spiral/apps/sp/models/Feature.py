from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.


class Feature(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    TYPE_UNIQUE = 1
    TYPE_MULTIPLE = 0
    CHOICE_TYPES = (
        (TYPE_UNIQUE, _(u'Valor Unico')),
        (TYPE_MULTIPLE, _(u'Valor multiple'))
    )

    type = models.SmallIntegerField(
        choices=CHOICE_TYPES,
        default=TYPE_UNIQUE
    )

    name = models.CharField(
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

    @staticmethod
    def get_data_features():
        data = []
        features = Feature.objects.filter(status=Feature.STATUS_ACTIVE)
        features = features.select_related('feature_value')
        for feature in features:
            tmp = []
            values = feature.feature_value_set.filter(status=FeatureValue.STATUS_ACTIVE)
            for value in values:
                tmp.append(
                        {
                            'value_id': value.id,
                            'value_name': value.name
                        }
                )
            data.append({
                'type': feature.get_type_display(),
                'feature_id': feature.id,
                'feature_name': feature.name,
                'feature_values':tmp
            })

        return data


class FeatureValue(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, _(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    feature = models.ForeignKey(
        'Feature',
        verbose_name=_('Carracteristica'),
        related_name='feature_value_set'
    )

    name = models.CharField(
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