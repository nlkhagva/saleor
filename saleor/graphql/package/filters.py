import django_filters

from ...unurshop.package import models
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param

######################
###### gaduur   ######
def filter_gaduur_search(qs, _, value):
    gaduur_fields = ["name"]
    qs = filter_by_query_param(qs, value, gaduur_fields)
    return qs


class GaduurFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_gaduur_search)

    class Meta:
        model = models.GaduurPackage
        fields = ["search"]


class GaduurFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = GaduurFilter

######################
###### packages ######
def filter_package_search(qs, _, value):
    package_fields=["name"]
    qs = filter_by_query_param(qs, value, package_fields)

    return qs

class PackageFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_package_search)

    class Meta:
        model = models.Package
        fields = ["search"]

class PackageFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = PackageFilter
