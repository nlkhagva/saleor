import django_filters

from ...unurshop.ushop.models import Shop
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param


def filter_ushop_search(qs, _, value):
    ushop_fields = ["description", "url", "name"]
    qs = filter_by_query_param(qs, value, ushop_fields)
    return qs


class UshopFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_ushop_search)

    class Meta:
        model = Shop
        fields = ["search"]


class UshopFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = UshopFilter
