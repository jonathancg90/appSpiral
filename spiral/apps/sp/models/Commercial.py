from django.utils.translation import ugettext_lazy as _
from django.db import models
import urllib2
from django.utils import simplejson

from apps.sp.models.Project import Project


class Commercial(models.Model):
    STATUS_TERMINATE = 2
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE,_(u'Inactivo')),
        (STATUS_TERMINATE,_(u'Terminado')),
        (STATUS_ACTIVE, _(u'Activo'))
    )

    name = models.CharField(
        verbose_name=_(u'Nombre'),
        max_length=50
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

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'

    def get_data_api_json(self):
        if self.project.project_code is not None:
            try:
                op = self.project.project_code[5:6]
                if op == "M":
                    url = 'http://192.168.1.3/sistemas/sisadmini/api/proyecto.php?codigo='+self.model_code
                else:
                    url = 'http://192.168.1.3/sistemas/barranco/api/proyecto.php?codigo='+self.model_code+'&'+'op='+op

                req = urllib2.Request(url, None, {'user-agent':'syncstream/vimeo'})
                opener = urllib2.build_opener()
                f = opener.open(req,timeout=1)
                api = simplejson.load(f)
                data = {
                    'nombre':api.get('nombre', None),
                    'productora':api.get('productora', None),
                    'agencia':api.get('agencia', None),
                    'realizadora': api.get('realizadora', None),
                    'response': True
                }
                return data
            except:
                pass

        data = {
            'response': False
        }
        return data

    @staticmethod
    def get_commercial_tag():
        return 'commercial_list'

    @property
    def realized(self):
        date = ''
        for detail in self.commercial_date_detail_set.all():
            date = date + detail.date.strftime("%d/%m/%Y") + ' | '
        return date

    @property
    def project(self):
        project = Project.objects.filter(commercial=self).exists()
        project = Project.objects.get(commercial=self).project_code if project else 'Ninguno'
        return project


class CommercialDateDetail(models.Model):

    commercial = models.ForeignKey(
        'commercial',
        verbose_name='Comercial',
        related_name='commercial_date_detail_set'
    )

    date = models.DateField(
        verbose_name='Fecha del comercial',
        null=False,
    )

    def __unicode__(self):
        return '%s %s' %(self.commercial, self.date)

    class Meta:
        app_label = 'sp'