from django.db import models


class PhotoCasting(models.Model):

    project = models.OneToOneField(
        'Project',
        primary_key=True
    )

    use_photo = models.ManyToManyField(
        'UsePhotos',
        verbose_name='Uso de las fotos',
    )

    type_casting = models.ForeignKey(
        'TypePhotoCasting',
        verbose_name='Tipo de casting',
        related_name='photo_casting_set',
    )

    class Meta:
        app_label = 'sp'

    @classmethod
    def get_detail_data(self, project):
        photo =  PhotoCasting.objects.get(project=project)
        detail_model = PhotoCastingDetailModel.objects.filter(photo_casting=photo)
        data = []
        for detail in detail_model:
            quantity_participate = PhotoCastingDetailParticipate.objects.filter(detail_model_id=detail.id).count()
            data.append({
                'id': detail.id,
                'cant': detail.quantity,
                'avaible': detail.quantity - quantity_participate,
                'profile': detail.profile,
                'model': detail.feature,
                'character': detail.get_character_display()
            })
        return data


class UsePhotos(models.Model):
    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, 'inactivo'),
        (STATUS_ACTIVE, 'activo')
    )

    name = models.CharField(
        verbose_name='Nombre',
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


class TypePhotoCasting(models.Model):

    STATUS_ACTIVE = 1
    STATUS_INACTIVE = 0
    CHOICE_STATUS = (
        (STATUS_INACTIVE, 'inactivo'),
        (STATUS_ACTIVE, 'activo')
    )

    name = models.CharField(
        verbose_name='Nombre',
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


class PhotoCastingDetailModel(models.Model):

    CHARACTER_PRINCIPAL = 1
    CHARACTER_SECONDARY = 0
    CHOICE_CHARACTER = (
        (CHARACTER_PRINCIPAL, 'Principal'),
        (CHARACTER_SECONDARY, 'Secundario')
    )

    photo_casting = models.ForeignKey(
        'PhotoCasting',
        related_name='photo_casting_detail_model_set',
    )

    quantity = models.SmallIntegerField()

    profile = models.CharField(
        verbose_name='Perfil',
        max_length=100
    )

    feature = models.CharField(
        verbose_name='Carracteristicas',
        max_length=200,
        null=True
    )

    character = models.SmallIntegerField(
        choices=CHOICE_CHARACTER,
        default=CHARACTER_PRINCIPAL,
        null=True
    )

    currency = models.ForeignKey(
        'Currency',
        verbose_name='Moneda',
        related_name='photo_casting_detail_model_set',
        null=True
    )

    budget_cost = models.DecimalField(
        verbose_name='Presupuesto',
        max_digits=10,
        decimal_places=2
    )

    observations = models.CharField(
        verbose_name='Observaciones',
        max_length=100,
        null=True
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        editable=False,
        auto_now=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sp'


class PhotoCastingDetailParticipate(models.Model):

    detail_model = models.ForeignKey(
        'PhotoCastingDetailModel',
        related_name='photo_casting_detail_participate_set',
    )

    model = models.ForeignKey(
        'Model',
        related_name='photo_casting_detail_participate_set',
    )

    created = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )

    modified = models.DateTimeField(
        auto_now_add=True
    )

    def __unicode__(self):
        return self.model.name_complete

    class Meta:
        app_label = 'sp'