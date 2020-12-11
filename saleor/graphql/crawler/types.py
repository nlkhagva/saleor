import graphene
from graphene import relay

from ...unurshop.crawler import models
from ..core.connection import CountableDjangoObjectType


class Crawler(CountableDjangoObjectType):
    class Meta:
        description = "Crawler"
        only_fields = [
            "id",
            "url",
            "completed",
            "crawled_at",
            "product_count",
            "json_data",
            "json_data_backup",
            "listSelection",
            "productSelection",
            "shop"
        ]
        interfaces = [relay.Node]
        model = models.Crawler
