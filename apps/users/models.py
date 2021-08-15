from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.roles = [User.ADMIN]
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    # User roles
    ADMIN = 0
    ROLE_QA = 1
    ROLE_TRANSLATOR = 2

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    roles = ArrayField(
        models.PositiveSmallIntegerField(),
        default=list,
        null=False
    )

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_admin(self):
        return self.ADMIN in self.roles

    USERNAME_FIELD = 'email'

    objects = UserManager()
