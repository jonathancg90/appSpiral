from django.utils.translation import ugettext_lazy as _
from django.db import models
import urllib2
import simplejson


class Commercial(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'inactivo')),
        (STATUS_ACTIVE, _(u'activo'))
    )

    name = models.CharField(
        verbose_name=_(u'Nombre'),
        max_length=50
    )
    realized = models.DateTimeField(
        verbose_name=_(u'Realizado'),
    )

    brand = models.ForeignKey(
        'Brand',
        verbose_name=_(u'Marca'),
        related_name='commercial_set',
    )
    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
        )

    project = models.ForeignKey(
        'Project',
        related_name='commercial_set',
        null=True,
        blank=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'

    def get_data_api_json(self):
        if self.project is not None:
            try:
                url = 'http://192.168.1.3/sistemas/proyspiral/api/model.php?codigo='+self.model_code
                req = urllib2.Request(url, None, {'user-agent':'syncstream/vimeo'})
                opener = urllib2.build_opener()
                f = opener.open(req,timeout=1)
                api = simplejson.load(f)
                data = {
                    'name':api.get('name'),
                    'productora':api.get('productora'),
                    'agencia':api.get('agencia'),
                    'realizadora': api.get('realizadora'),
                    'response': True
                }
                return data
            except:
                pass

        data = {
            'response': False
        }
        return data