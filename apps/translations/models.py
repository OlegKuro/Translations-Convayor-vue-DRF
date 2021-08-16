from django.db import models
from utils.models import CreatedByMixin, CreateAtMixin, ModifiedAtMixin
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from datetime import datetime


class TranslationQuerySet(models.QuerySet):
    """QS extension"""

    def without_overdue(self):
        return self.exclude(deadline__lt=datetime.now())


class Translation(CreatedByMixin, CreateAtMixin, ModifiedAtMixin):

    NEW = 0
    IN_PROGRESS = 1
    NEEDS_QA = 2
    COMPLETED = 3

    STATE_CHOICES = (
        (NEW, _('new')),
        (IN_PROGRESS, _('in progress')),
        (NEEDS_QA, _('needs_qa')),
        (COMPLETED, _('completed')),
    )

    origin = models.TextField(blank=False, help_text='Origin text to translate')
    translation = models.TextField(blank=False, help_text='translation variant')
    translator_comment = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, db_index=True, default=NEW)

    translator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='translations', null=True,
                                   on_delete=models.SET_NULL)
    assigned_qa = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='inspected_translations', null=True,
                                    on_delete=models.SET_NULL)

    objects = TranslationQuerySet.as_manager()
