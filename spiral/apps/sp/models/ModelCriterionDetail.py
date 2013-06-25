from django.db import models
from django.utils.translation import ugettext_lazy as _


class ModelCriterionDetail(models.Model):

    LEVEL_AMATEUR = 1
    LEVEL_STUDENT = 2
    LEVEL_PROFESSIONAL = 3
    CHOICE_LEVEL = (
        (LEVEL_AMATEUR,_(u'Aficionado')),
        (LEVEL_STUDENT, _(u'Estudiante')),
        (LEVEL_PROFESSIONAL, _(u'Profesional')),
    )
    model = models.ForeignKey(
        'Model',
        related_name='model_criterion_detail_set'
    )

    criterion_detail = models.ForeignKey(
        'CriterionDetail',
        related_name='model_criterion_detail_set'
    )
    observations = models.CharField(
        max_length=300
    )
    level = models.SmallIntegerField(
        choices=CHOICE_LEVEL,
        default=None,
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
        return self.description

    class Meta:
        app_label = 'sp'