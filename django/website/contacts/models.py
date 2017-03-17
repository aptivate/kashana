import os.path

from django.db.models import (
    CharField, TextField, EmailField,
    FileField, DateTimeField, BooleanField,
    ImageField, ForeignKey, OneToOneField, Model
)
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission)
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from django.utils.six import python_2_unicode_compatible

from main.upload_handler import UploadToHandler
from .countries import COUNTRIES, NATIONALITIES


def get_user_fields(instance):
    return (instance.business_email, instance.last_name, instance.first_name)


@deconstructible
class PictureUploadHandler(object):
    path_base = ''

    def __init__(self, path_base):
        self.path_base = path_base

    def __call__(self, instance, filename):
        name = "_".join([instance.last_name, instance.first_name]).strip('_')
        prefix = name if name else instance.business_email
        new_filename = "{0}_{1}".format(prefix, filename)
        new_path = os.path.join(self.path_base, new_filename)
        return new_path


# Managers
class UserManager(BaseUserManager):
    def _create_user(self, business_email=None, password=None,
                     is_active=True, is_staff=False, is_superuser=False,
                     **extra_fields):
        now = timezone.now()
        if not business_email:
            raise ValueError('The given business_email must be set')
        email = UserManager.normalize_email(business_email)
        user = self.model(business_email=email, is_staff=is_staff,
                          is_active=is_active, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, business_email=None, password=None, **extra_fields):
        return self._create_user(business_email, password, **extra_fields)

    def create_superuser(self, business_email, password, **extra_fields):
        return self._create_user(business_email, password, is_staff=True,
                                 is_superuser=True, **extra_fields)


# Models
class User(AbstractBaseUser, PermissionsMixin):
    # Account info
    business_email = EmailField(unique=True)
    is_staff = BooleanField(
        verbose_name='staff status',
        default=False,
        help_text=('Designates whether the user can log into this admin '
                   'site.'))
    is_active = BooleanField(
        verbose_name='active',
        default=True,
        help_text=('Designates whether this user should be treated as '
                   'active. Unselect this instead of deleting accounts.'))
    date_joined = DateTimeField(default=timezone.now)

    # general contact information
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)

    # Managers and book-keeping

    USERNAME_FIELD = 'business_email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def get_full_name(self):
        return u"{0} {1}".format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __unicode__(self):
        return self.get_full_name()

    @property
    def email(self):
        return self.business_email

    @property
    def preferences(self):
        try:
            preferences = self._preferences
        except UserPreferences.DoesNotExist:
            preferences = UserPreferences.objects.create(user=self)
        return preferences


class UserPreferences(Model):
    user = OneToOneField(User, related_name='_preferences')
    last_viewed_logframe = ForeignKey('logframe.LogFrame', null=True)
    last_viewed_organization = ForeignKey('organizations.Organization', null=True)

@python_2_unicode_compatible
class NameOnlyPermission(Permission):
    class Meta:
        proxy = True

    def __str__(self):
        return "Can {0}".format(self.name.lower())
