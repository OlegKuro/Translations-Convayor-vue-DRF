from django_filters import rest_framework as filters

from translations.models import Translation


class TranslationFilter(filters.FilterSet):
    state = filters.MultipleChoiceFilter(
        choices=Translation.STATE_CHOICES,
    )
    active = filters.BooleanFilter(method='without_overdue')

    class Meta:
        model = Translation
        fields = (
            'state',
            'active',
        )

    @property
    def qs(self):
        qs = super().qs
        if 'assigned_to_me' in self.request.GET:
            qs = self.assigned_to_me(qs, self.request.GET['assigned_to_me'].lower() not in ('0', 'false'))
        return qs

    def without_overdue(self, queryset, _, value):
        if value:
            queryset = queryset.without_overdue()
        return queryset

    def assigned_to_me(self, qs, value):
        if value:
            qs = self._meta.model.objects.assigned_to_me(self.request.user)
        return qs
