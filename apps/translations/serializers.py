from rest_framework import serializers
from translations.models import Translation


class TranslationListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = (
            'origin',
            'translation',
            'translator_comment',
            'deadline',
            'state',
            'modified_at',
            'created_at',
        )
        extra_kwargs = {
            'translation': {'read_only': True},
            'translator_comment': {'read_only': True},
            'state': {'read_only': True},
        }
