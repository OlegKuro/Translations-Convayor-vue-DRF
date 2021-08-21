from rest_framework import serializers
from translations.models import Translation
from users.models import User


class TranslationListCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = (
            'id',
            'origin',
            'translation',
            'comment',
            'deadline',
            'state',
            'modified_at',
            'created_at',
            'assigned_qa',
            'translator',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'translation': {'read_only': True},
            'comment': {'read_only': True},
            'state': {'read_only': True},
        }


class TranslationRetrieveUpdateSerializer(TranslationListCreateSerializer):
    translation = serializers.CharField(allow_blank=True)
    assigned_qa = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    translator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)

    class Meta:
        model = Translation
        fields = TranslationListCreateSerializer.Meta.fields + (
            'assigned_qa',
            'translator',
        )
        extra_kwargs = {}

    @property
    def validated_data(self):
        data = super().validated_data
        request = self.context.get('request')
        if data['state'] == Translation.IN_PROGRESS and data.get('translator') is None:
            data['translator'] = request.user
        if data['state'] == Translation.VERIFYING and data.get('assigned_qa') is None:
            data['assigned_qa'] = request.user
        return data


class TranslationStateChangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Translation
        fields = (
            'state',
            'comment',
            'translation',
        )
        extra_kwargs = {
            'translation': {'allow_blank': True},
        }

    def is_valid(self, raise_exception=False):
        result = super().is_valid(raise_exception)
        request = self.context.get('request')
        if self.instance.state == Translation.IN_PROGRESS and 'translation' not in request.data:
            raise serializers.ValidationError('You should propose some translation')
        if self.instance.state == Translation.IN_PROGRESS and request.data['state'] == Translation.VERIFYING \
                and self.instance.assigned_qa is None:
            raise serializers.ValidationError('Forbidden state shift')
        return result

    def save(self, **kwargs):
        request = self.context.get('request')
        validated_data = {**self.validated_data, **kwargs}

        Translation.objects.validate_change_state(self.instance, request.user, validated_data['state'])
        self.instance.set_assignees(request.user, validated_data['state'])

        self.instance = self.update(self.instance, validated_data)

        return self.instance
