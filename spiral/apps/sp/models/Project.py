from django.db import models
from django.utils.translation import ugettext_lazy as _


class Project(models.Model):

    TYPE_EXTRA = 2
    TYPE_CASTING = 1
    CHOICE_TYPE = (
        (TYPE_EXTRA, _(u'extra')),
        (TYPE_CASTING, _(u'casting'))
    )

    project_code = models.CharField(
        max_length=9,
        unique=True,
    )

    project_name = models.CharField(
        max_length=45
    )
    project_type = models.SmallIntegerField(
        choices=CHOICE_TYPE,
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

