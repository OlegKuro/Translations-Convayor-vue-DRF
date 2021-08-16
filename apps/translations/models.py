from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.serializers import ValidationError

from users.models import User
from utils.models import CreatedAtMixin, ModifiedAtMixin


class TranslationManager(models.Manager):

    def validate_change_state(self, instance, user, new_state):
        """
        :raises ValidationError
        """
        if User.ADMIN not in user.roles:
            if not any([(instance.state in self.model.ROLES_TO_AVAILABLE_STATES[role]) for role in user.roles]):
                raise ValidationError('You have no permission to change state')
            if new_state not in self.model.STATE_FLOW_FROM_TO[instance.state]:
                raise ValidationError('You can not change state this way')
            if all(
                    [
                        instance.state == self.model.IN_PROGRESS,
                        instance.assigned_qa is not None,
                        new_state == self.model.NEEDS_QA,
                    ]
            ):
                raise ValidationError('You should change state to Verifying')


class TranslationQuerySet(models.QuerySet):
    """QS extension"""

    def without_overdue(self):
        return self.exclude(deadline__lt=datetime.now())


class Translation(CreatedAtMixin, ModifiedAtMixin):
    NEW = 0
    IN_PROGRESS = 1
    NEEDS_QA = 2
    VERIFYING = 3
    COMPLETED = 4

    STATE_CHOICES = (
        (NEW, _('new')),
        (IN_PROGRESS, _('in progress')),
        (NEEDS_QA, _('needs_qa')),
        (VERIFYING, _('verifying')),
        (COMPLETED, _('completed')),
    )

    ROLES_TO_AVAILABLE_STATES = {
        User.ADMIN: {NEW, IN_PROGRESS, NEEDS_QA, VERIFYING, COMPLETED},
        User.ROLE_QA: {NEEDS_QA, VERIFYING},
        User.ROLE_TRANSLATOR: {NEW, IN_PROGRESS},
    }

    STATE_FLOW_FROM_TO = {
        NEW: {IN_PROGRESS},
        IN_PROGRESS: {NEEDS_QA, VERIFYING},
        NEEDS_QA: {VERIFYING},
        VERIFYING: {IN_PROGRESS, COMPLETED, NEW},
        COMPLETED: set(),
    }

    origin = models.TextField(blank=False, help_text='Origin text to translate')
    translation = models.TextField(blank=False, help_text='translation variant')
    comment = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True)
    state = models.PositiveSmallIntegerField(choices=STATE_CHOICES, db_index=True, default=NEW)

    translator = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='translations', null=True,
                                   on_delete=models.SET_NULL)
    assigned_qa = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='inspected_translations', null=True,
                                    on_delete=models.SET_NULL)

    objects = TranslationManager.from_queryset(TranslationQuerySet)()

    def set_assignees(self, user, new_state):
        """Sets assignee (translator or qa) to current user"""
        if new_state == self.IN_PROGRESS and self.state == self.NEW:
            # translator took the task
            self.translator = user
        if new_state == self.VERIFYING and self.state == self.NEEDS_QA:
            # qa took task
            self.assigned_qa = user
        if new_state == self.NEW and self.state == self.VERIFYING:
            # qa returned the task into the list.
            # qa is still assigned to the task and will receive it as soon as it is done
            self.translator = None
        return self
