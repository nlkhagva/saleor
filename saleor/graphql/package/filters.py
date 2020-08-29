import django_filters

from ...unurshop.package.models import GaduurPackage
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param


def filter_gaduur_search(qs, _, value):
    gaduur_fields = ["name"]
    qs = filter_by_query_param(qs, value, gaduur_fields)
    return qs


class GaduurFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_gaduur_search)

    class Meta:
        model = GaduurPackage
        fields = ["search"]


class GaduurFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = GaduurFilter
