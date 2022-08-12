from django.db import models
from django.utils.translation import gettext_lazy as _


class FeatureBase(models.Model):
    """ Common fields for both categories and features. """

    ONLY_MISSION = 1
    ONLY_PROFILE = 2
    BOTH = 3

    SCOPE = (
        (ONLY_MISSION, _('Only on mission description')),
        (ONLY_PROFILE, _('Only on entrepreneur profile')),
        (BOTH, _('On both mission & profile'))
    )

    #: Define if a feature or a feature category is relevant on mission description or entrepreneur profile.
    scope = models.PositiveSmallIntegerField(choices=SCOPE, default=BOTH, verbose_name=_('scope'))

    class Meta:
        abstract = True


class FeatureCategory(FeatureBase):
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


class Feature(FeatureBase):
    """ Specific features to describe mission requirements & entrepreneur's skills. """

    description = models.CharField(max_length=300, unique=True, verbose_name=_('description'))
    category = models.ForeignKey(FeatureCategory, on_delete=models.PROTECT, related_name="features")

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _('Feature')
        verbose_name_plural = _('Features')


