from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    cod_emp = models.CharField(max_length=10)

    class Meta:
        app_label = 'sp'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])