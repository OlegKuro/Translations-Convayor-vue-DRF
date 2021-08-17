from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.filters import OrderingFilter
from translations.models import Translation
from translations.filters import TranslationFilter
from translations.serializers import TranslationListCreateSerializer, TranslationRetrieveUpdateSerializer,\
    TranslationStateChangeSerializer
from django_filters.rest_framework import DjangoFilterBackend
from translations.permissions import HasTranslationModelPermission
from utils.permissions import IsObjectAdmin
from users.models import User


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


class TranslationRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = TranslationRetrieveUpdateSerializer
    queryset = Translation.objects.all()
    permission_classes = (HasTranslationModelPermission,)

    def flow_update(self, request):
        self.serializer_class = TranslationStateChangeSerializer
        return super().update(request, partial=True)

    def update(self, request, *args, **kwargs):
        if User.ADMIN in request.user.roles:
            return super().update(request, *args, **kwargs)
        return self.flow_update(request)

