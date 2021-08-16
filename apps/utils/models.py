from django.db import models
from django.utils import timezone
from django.conf import settings


class CreateAtMixin(models.Model):
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        abstract = True


class ModifiedAtMixin(models.Model):
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CreatedByMixin(models.Model):
    created_by = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class ModifiedBy(models.Model):
    modified_bt = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True
