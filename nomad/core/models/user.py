from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
import string
from .company import Company
from .features import Feature


class UserManager(BaseUserManager):
    """ A DB manager for user model using the email address in place of a username. """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(
                _('Email value is mandatory to create a new user'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, type=User.ADMIN, **extra_fields)


class User(AbstractUser):
    """ Specific user model which remove the username field and use the email as user's identifier. """
    def group_based_upload_to(instance, filename):

        return f"files/{instance.last_name}/{filename}"

    #: Nomad administrator
    ADMIN = 0
    #: Company user
    COMPANY = 1
    #: Entrepreneur
    ENTREPRENEUR = 2

    TYPES = (
        (ADMIN, _('Administrator')),
        (COMPANY, _('Company user')),
        (ENTREPRENEUR, _('Entrepreneur')),
    )

    #: young graduate
    FIRST = 0
    #: 0 to 3 years
    SECOND = 1
    #: 4 to 8 years
    THIRD = 2
    # more than 8 years
    FOURTH = 3

    EXPERIENCES = (
        (FIRST, _('Young graduate')),
        (SECOND, _('0 to 3 years of experience')),
        (THIRD, _('4 to 8 years of experience')),
        (FOURTH, _('more than 8 years of experience')),
    )

    #: We don't use the username, remove this field from the base model.
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone']
    objects = UserManager()

    #: Set the email field as user identifier and set it unique.
    email = models.EmailField(_('email address'), unique=True)
    #: First name of the user, set as mandatory.
    first_name = models.CharField(max_length=150, verbose_name=_('first name'))
    #: Last name of the user, set as mandatory.
    last_name = models.CharField(max_length=150, verbose_name=_('last name'))
    #: Phone number, required for each user company, optional for other types of users
    phone = models.CharField(max_length=20, verbose_name=_('phone number',),
                             help_text=_('required for company users and entrepreneur'))
    #: Type of the user
    type = models.PositiveSmallIntegerField(
        choices=TYPES, default=ENTREPRENEUR, verbose_name=_('type of user'))
    #: Driving license of the user
    driving_license = models.BooleanField(
        default=False, verbose_name=_('driving license'))
    #: Company of the user if needed
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True,
                                verbose_name=_('company'), related_name='users')

    #: Features for entrepreneur users
    features = models.ManyToManyField(
        Feature, related_name='users', blank=True, verbose_name=_('features'))

    year_experience = models.PositiveSmallIntegerField(
        choices=EXPERIENCES, default=FIRST, verbose_name=_('years of experience'))

    siret = models.CharField(max_length=9, verbose_name=_(
        'SIRET number'), help_text=_('must be 9 characters wide'), blank=True,)

    files = models.FileField(upload_to=group_based_upload_to, blank=True, verbose_name=_(
        'files required'))

    @property
    def is_admin(self):
        return self.type == User.ADMIN

    @property
    def is_company(self):
        return self.type == User.COMPANY

    @property
    def is_entrepreneur(self):
        return self.type == User.ENTREPRENEUR

    @property
    def is_complete(self):
        """ Returns True if an entrepreneur profile is complete, i.e. this user has features, availabilities and
            work locations set in the database. If the user is not an entrepreneur profile, raises ValueError.
        """
        if not self.is_entrepreneur:
            raise ValueError("is_complete not available on this user")
        return self.features.count() > 0 and self.availabilities.count() > 0 and self.locations.count() > 0

    def clean(self):
        super().clean()
        if self.is_company:
            if not self.company:
                raise ValidationError(_('a company user must be attached to an existing company'))
            if not self.phone:
                raise ValidationError(_('company users must have a valid phone number'))

        if self.siret:
            if len(self.siret) != 9:
                raise ValidationError(_('SIRET number must be 9 characters wide'))
            if any([c not in string.digits for c in self.siret]):
                raise ValidationError(_('SIRET number should contain only digits characters'))

    def save(self, *args, **kwargs):
        self.full_clean()
        # clean fields
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().title()
        self.email = self.email.strip().lower()
        super(User, self).save(*args, **kwargs)
