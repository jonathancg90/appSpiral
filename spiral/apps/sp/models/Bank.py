from django.db import models


class Bank(models.Model):

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

    status = models.SmallIntegerField(
        choices=CHOICE_STATUS,
        default=STATUS_ACTIVE
    )