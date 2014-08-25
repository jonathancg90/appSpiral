from django.db import models


class Company(models.Model):

    STATUS_ACTIVE = 1
    STATUS_DELETE = 2
    STATUS_INACTIVE = 3
    CHOICE_STATUS = (
        (STATUS_ACTIVE, 'extra'),
        (STATUS_INACTIVE, 'casting'),
        (STATUS_DELETE, 'casting')
    )

    name = models.CharField(
        verbose_name='Nombre',
        max_length=70
    )

    ruc = models.CharField(
        verbose_name='RUC',
        max_length=10,
    )

    address = models.CharField(
        verbose_name='Direccion',
        max_length=100,
    )

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )

    def __unicode__(self):
        return '%s %s' %(self.name, self.ruc)

    class Meta:
        app_label = 'sp'


class CompanyDetailAccount(models.Model):

    bank = models.ForeignKey(
        'Bank',
        verbose_name='Banco',
        related_name='company_detail_account_set'
    )

    account = models.CharField(
        verbose_name='Numero de cuenta',
        max_length=30,
    )

    def __unicode__(self):
        return '%s %s' %(self.bank.name, self.account)

    class Meta:
        app_label = 'sp'