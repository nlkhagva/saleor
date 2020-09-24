import django_filters

from ...unurshop.crawler import models
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param


def filter_crawler_search(qs, _, value):
    crawler_fields = ["url", "shop", "completed"]
    qs = filter_by_query_param(qs, value, crawler_fields)
    return qs


class CrawlerFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method=filter_crawler_search)

    class Meta:
        model = models.Crawler
        fields = ["search"]


class CrawlerFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = CrawlerFilter
