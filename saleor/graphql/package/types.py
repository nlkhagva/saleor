import graphene
from graphene import relay

from ...unurshop.package import models

from ..core.connection import CountableDjangoObjectType
from ..core.types import (
    Image
)


class Gaduur(CountableDjangoObjectType):
    class Meta:
        description = """A static page that can be manually added by a gaduur
               operator through the dashboard."""
        only_fields = [
            "id",
            "name",
            "shipping_type",
            "is_published",
            "publication_date",
            "start_date",
            "end_date",
        ]
        interfaces = [relay.Node]
        model = models.GaduurPackage

    @staticmethod
    def resolve_available_on(root: models.GaduurPackage, _info):
        return root.publication_date

    @staticmethod
    def resolve_is_visible(root: models.GaduurPackage, _info):
        return root.is_published

class Package(CountableDjangoObjectType):
    class Meta:
        description ="package"
        only_fields = [
            "id",
            "name",
            "status",
            "gaduur",
            "user",
            "shipping_address",
            "sender_address",
            "upostPK",
            "net_weight",
            "gross_weight",
            "width",
            "height",
            "length",
            "currency",
            "total_gross_amount"
        ]
        interfaces = [relay.Node]
        model = models.Package

