from django.dispatch import receiver
from django.db.models.signals import post_save
from translations.models import Translation
from utils.websockets import broadcast


@receiver(post_save, sender=Translation, dispatch_uid='websockets_detect_new_tasks')
def websockets_detect_new_tasks(sender, instance, created, **kwargs):
    """ Indicates that new task is available (for QA or Translator) """

    if instance.state in (Translation.NEEDS_QA, Translation.NEW):
        broadcast('tasks', 'available', {
            'id': instance.id,
            'state': instance.state,
        })
