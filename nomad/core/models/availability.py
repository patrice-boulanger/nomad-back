from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .user import User


class Availability(models.Model):
    """ Availability time slot for an entrepreneur user """

    #: Start date/time of the time slot
    start = models.DateTimeField(verbose_name=_('start'))
    #: End date/time of the time slot
    end = models.DateTimeField(verbose_name=_('end'))
    #: Affected user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="availabilities")

    def __str__(self):
        return str(self.start) + " - " + str(self.end)

    def clean(self):
        super().clean()
        if not self.user.is_entrepreneur:
            raise ValidationError('availability time slots can only be affected to entrepreneur users')
        if self.end < self.start:
            raise ValidationError('start date must be less than end date')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ("start",)
        verbose_name = _("Availability timeslot")
        verbose_name_plural = _("Availability timeslots")