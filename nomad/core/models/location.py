import string
import json

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.utils import zipcode_extract

from .user import User


class WorkLocation(models.Model):
    zipcode = models.CharField(max_length=5, verbose_name=_('zipcode'))
    city = models.CharField(default=None, max_length=100, blank=True, null=True, verbose_name=_('city'),
                            editable=False, help_text=_('this field is auto-completed'))
    department = models.PositiveIntegerField(default=None, blank=True, null=True, verbose_name=_('department'),
                                             editable=False, help_text=_('this field is autocompleted'))
    department_name = models.CharField(default=None, max_length=100, blank=True, null=True, editable=False,
                                       verbose_name=_('department name'), help_text=_('this field is autocompleted'))
    region = models.CharField(default=None, max_length=100, blank=True, null=True, editable=False,
                              verbose_name=_('region'), help_text=_('this field is autocompleted'))
    longitude = models.FloatField(default=None, blank=True, null=True, editable=False,
                                  verbose_name=_('longitude'), help_text=_('this field is autocompleted'))
    latitude = models.FloatField(default=None, blank=True, null=True, editable=False,
                                 verbose_name=_('latitude'), help_text=_('this field is autocompleted'))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="locations")

    def __str__(self):
        return self.zipcode

    def clean(self):
        super().clean()
        if not self.user.is_entrepreneur:
            raise ValidationError('locations can only be affected to entrepreneur users')
        if any([c not in string.digits for c in self.zipcode]):
            raise ValidationError("the zipcode must be all numeric")

    def save(self, *args, **kwargs):
        self.full_clean()

        try:
            city, dpt, dpt_name, region, lat, long = zipcode_extract(self.zipcode)
            self.city = city
            self.department = dpt
            self.department_name = dpt_name
            self.region = region
            self.latitude = lat
            self.longitude = long
        except Exception:
            pass

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('zipcode',)
        verbose_name = _('Work location')
        verbose_name_plural = _('Work locations')
