from django.db import models
from django.utils.translation import gettext_lazy as _


class FeatureCategory(models.Model):
    """ Feature categories allow to group features """

    name = models.CharField(max_length=200, unique=True, verbose_name=_('name'))
    multiple_choices = models.BooleanField(default=False, verbose_name=_('multiple choices'))
    rank = models.PositiveSmallIntegerField(default=999, verbose_name=_('display order'))

    def __str(self):
        return self.name

    class Meta:
        ordering = ('rank', 'name',)
        verbose_name = _('Features category')
        verbose_name_plural = _('Features categories')


class Feature(models.Model):
    """ Specific features to describe mission requirements & entrepreneur's skills. """

    description = models.CharField(max_length=300, unique=True, verbose_name=_('description'))
    category = models.ForeignKey(FeatureCategory, on_delete=models.PROTECT, related_name="features")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')


