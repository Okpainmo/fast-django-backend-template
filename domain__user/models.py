from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


class User(models.Model):
    """
    Custom User model - unrelated to Django's user model.
    Feel free to extend Django user model if you wish
    """

    name = models.CharField(
        _('name'),
        max_length=100,
        validators=[MinLengthValidator(2), MaxLengthValidator(100)],
        blank=True,
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[^\s]*$', message='Email cannot contain spaces.', code='invalid_email'
            )
        ],
    )
    password = models.CharField(
        _('password'),
        max_length=255,
        null=True,  # Allow null values for existing records
        blank=True,
    )
    access_token = models.CharField(
        _('access token'),
        max_length=255,
        null=True,  # Allow null values for existing records
        blank=True,
    )
    refresh_token = models.CharField(
        _('refresh token'),
        max_length=255,
        null=True,  # Allow null values for existing records
        blank=True,
    )
    is_admin = models.BooleanField(_('admin status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def __str__(self):
        return str(self.email)
