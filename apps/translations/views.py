from rest_framework.generics import ListCreateAPIView
from rest_framework.filters import OrderingFilter
from translations.models import Translation
from translations.filters import TranslationFilter
from translations.serializers import TranslationListCreateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from utils.permissions import IsObjectAdmin


class TranslationIndexCreateApiView(ListCreateAPIView):
    permission_classes = (
        IsObjectAdmin,
    )
    queryset = Translation.objects.all()
    serializer_class = TranslationListCreateSerializer
    filter_class = TranslationFilter
    filter_backends = (
        OrderingFilter,
        DjangoFilterBackend,
    )
    ordering_fields = (
        'created_at',
        'modified_at',
    )
    ordering = '-modified_at'
