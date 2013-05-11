from django.utils.translation import ugettext_lazy as _
from django.db import models
from apps.sp.models.Project import Project
from apps.sp.models.Brand import Brand

class Commercial(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    name = models.CharField(
        verbose_name=_(u'Nombre'),
        max_length = 50
	    )
    realized = models.DateTimeField()
	
    brand_id = models.ForeignKey(
	    Brand
	    )
    status = models.SmallIntegerField(
	    choices= CHOICE_STATUS,
        default = STATUS_ACTIVE
        )

    project_id = models.ForeignKey(
        "Project",
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'