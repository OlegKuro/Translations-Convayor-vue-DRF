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

    def without_overdue(self, queryset, _, value):
        if value:
            queryset = queryset.without_overdue()
        return queryset
