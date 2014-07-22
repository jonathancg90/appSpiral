from django.db import models


class Payment(models.Model):

    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    conditions = models.TextField(
        verbose_name='Condiciones',
        null=True,
    )

    client = models.ForeignKey(
        'Client',
        verbose_name='Facturar a',
        related_name='casting_set',
        null=True
    )

    class Meta:
        app_label = 'sp'

    class Meta:
        app_label = 'sp'