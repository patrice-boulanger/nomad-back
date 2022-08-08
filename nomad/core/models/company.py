import string

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Company(models.Model):

    PRIVATE = 0
    PUBLIC = 1
    HOSPITAL = 2
    CLINIC = 3
    CHARITY = 4

    TYPES = (
        (PRIVATE, _('private company')),
        (PUBLIC, _('public company')),
        (HOSPITAL, _('hospital')),
        (CLINIC, _('clinic')),
        (CHARITY, _('charity')),
    )

    #: Name of the company
    name = models.CharField(max_length=100, verbose_name=_('company name'))
    #: SIRET number
    siret = models.CharField(max_length=9, verbose_name=_('SIRET number'), help_text=_('must be 9 characters wide'))
    #: Type of the company
    type = models.PositiveSmallIntegerField(choices=TYPES, verbose_name=_('type of company'))
    #: Postal address
    address = models.CharField(max_length=300, verbose_name=_('postal address'))
    #: Zip code
    zipcode = models.CharField(max_length=5, verbose_name=_('zipcode'))
    #: City
    city = models.CharField(max_length=100, verbose_name=_('city'))
    #: VAT excluded
    vat_excluded = models.BooleanField(default=False, verbose_name=_('Is VAT excluded'))

    def clean(self):
        self.name = self.name.strip().title()

        if len(self.siret) != 9:
            raise ValidationError(_('SIRET number must be 9 characters wide'), )
        if any([c not in string.digits for c in self.siret]):
            raise ValidationError(_('SIRET number should contain only digits characters'))

        if self.vat_excluded and self.type != self.CHARITY:
            raise ValidationError(_('only charity companies can be VAT excluded'))

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
