from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    # Custom fields
    is_admin = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)


    # Additional fields to manage user groups and permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    # Meta class for model options
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ['id']
