from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

from .company import Company


class UserManager(BaseUserManager):
    """ A DB manager for user model using the email address in place of a username. """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('Email value is mandatory to create a new user'))

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

    #: We don't use the username, remove this field from the base model.
    username = None
    #: Set the email field as user identifier and set it unique.
    email = models.EmailField(_('email address'), unique=True)
    #: First name of the user, set as mandatory.
    first_name = models.CharField(max_length=150, verbose_name=_('first name'))
    #: Last name of the user, set as mandatory.
    last_name = models.CharField(max_length=150, verbose_name=_('last name'))
    #: Phone number, required for each user company, optional for other types of users
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('phone number'),
                             help_text=_('required for company users'))
    #: Type of the user
    type = models.PositiveSmallIntegerField(choices=TYPES, default=ENTREPRENEUR, verbose_name=_('type of user'))
    #: Company of the user if needed
    company = models.ForeignKey(Company, on_delete=models.PROTECT, blank=True, null=True,
                                verbose_name=_('company'), related_name='users')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    @property
    def is_admin(self):
        return self.type == User.ADMIN

    @property
    def is_company(self):
        return self.type == User.COMPANY

    @property
    def is_entrepreneur(self):
        return self.type == User.ENTREPRENEUR

    def clean(self):
        super().clean()

        if self.is_company:
            if not self.company:
                raise ValidationError(_('a company user must be attached to an existing company'))
            if not self.phone:
                raise ValidationError(_('company users must have a valid phone number'))

    def save(self, *args, **kwargs):
        self.full_clean()

        # clean fields
        self.first_name = self.first_name.strip().title()
        self.last_name = self.last_name.strip().title()
        self.email = self.email.strip().lower()

        super(User, self).save(*args, **kwargs)
