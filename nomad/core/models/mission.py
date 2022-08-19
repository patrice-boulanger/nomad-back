import logging
import string
import logging

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import Company, Feature
from core.utils import zipcode_extract


logger = logging.getLogger("application")

class Mission(models.Model):

    #: Title of the mission.
    title = models.CharField(max_length=300, verbose_name=_('title'))
    #: Complete description of the mission
    description = models.TextField(verbose_name=_('description'))
    #: Start date of the mission
    start = models.DateField(verbose_name=_('start date'))
    #: End date of the mission
    end = models.DateField(verbose_name=_('end date'))
    #: Company owning the mission
    company = models.ForeignKey(Company, on_delete=models.PROTECT, verbose_name=_('company'), related_name="missions")

    #: Features of the mission
    features = models.ManyToManyField(Feature, related_name="missions", blank=True, verbose_name=_('features'))

    #: Location of the mission
    zipcode = models.CharField(max_length=5, verbose_name=_('zipcode'))
    #: City of the mission, inferred from the zipcode
    city = models.CharField(default=None, max_length=100, blank=True, null=True, verbose_name=_('city'),
                            editable=False, help_text=_('this field is auto-completed'))
    def __str__(self):
        return "M-" + str(self.pk).rjust(5, '0')

    @property
    def state(self):
        today = timezone.now().date()
        if today < self.start:
            return _('pending')
        elif today > self.end:
            return _('expired')
        else:
            return _('overdue')

    def clean(self):
        super().clean()
        if any([c not in string.digits for c in self.zipcode]):
            raise ValidationError(_("the zipcode must be all numeric"))
        if self.start > self.end:
            raise ValidationError(_("end date must less than start date"))
        self.title = self.title.strip()
        try:
            self.city, d, dn, r, la, lo = zipcode_extract(self.zipcode)
        except Exception as e:
            logger.warning(f"cannot expand zipcode {self.zipcode} for mission {self.pk}: {str(e)}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('mission')
        verbose_name_plural = _('missions')
