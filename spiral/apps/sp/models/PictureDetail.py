from django.db import models
from apps.fileupload.models import Picture


class PictureDetailFeature(models.Model):

    picture = models.ForeignKey(
        Picture,
        related_name='picture_detail_feature_set',
    )

    feature_value = models.ForeignKey(
        'MediaFeatureValue',
        related_name='picture_detail_feature_set',
    )

    class Meta:
        app_label = 'sp'


class MediaFeature(models.Model):

    STATUS_ACTIVE = 1
    STATUS_DELETE = 2
    STATUS_INACTIVE = 3
    CHOICE_STATUS = (
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_INACTIVE, 'Inactivo'),
        (STATUS_DELETE, 'Eliminado')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=70
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'


class MediaFeatureValue(models.Model):

    STATUS_ACTIVE = 1
    STATUS_DELETE = 2
    STATUS_INACTIVE = 3
    CHOICE_STATUS = (
        (STATUS_ACTIVE, 'Activo'),
        (STATUS_INACTIVE, 'Inactivo'),
        (STATUS_DELETE, 'Eliminado')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=70
    )

    media_feature = models.ForeignKey(
        'MediaFeature',
        verbose_name='Carracteristica',
        related_name='media_feature_value_set'
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'