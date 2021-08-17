import itertools

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from translations.filters import TranslationFilter
from translations.models import Translation
from translations.permissions import HasTranslationModelPermission
from translations.serializers import TranslationListCreateSerializer, TranslationRetrieveUpdateSerializer, \
    TranslationStateChangeSerializer
from users.models import User
from utils.permissions import IsObjectAdmin


class TranslationIndexCreateApiView(ListCreateAPIView):
    permission_classes = (
        IsAuthenticated, IsObjectAdmin
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

    def get_queryset(self):
        qs = super().get_queryset()
        if User.ADMIN not in self.request.user.roles:
            # not admins are available to see their state and assigned to them
            user = self.request.user
            available_states = [states for role, states in Translation.ROLES_TO_AVAILABLE_STATES.items()
                                if role in user.roles]
            available_states = list(set(itertools.chain(*available_states)))
            print(available_states)
            qs = qs.filter(Q(state__in=available_states) | Q(assigned_qa=user) | Q(translator=user))
        return qs


class TranslationRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = TranslationRetrieveUpdateSerializer
    queryset = Translation.objects.all()
    permission_classes = (HasTranslationModelPermission,)

    def flow_update(self, request):
        self.serializer_class = TranslationStateChangeSerializer
        return super().update(request, partial=True)

    def update(self, request, *args, **kwargs):
        if User.ADMIN in request.user.roles:
            kwargs['partial'] = True
            return super().update(request, *args, **kwargs)
        return self.flow_update(request)
