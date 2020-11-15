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
            "packages",
            "status",
            "start_date",
            "end_date",
            "received_date",
            "tracking_number"
        ]
        interfaces = [relay.Node]
        model = models.GaduurPackage

    @staticmethod
    def resolve_available_on(root: models.GaduurPackage, _info):
        return root.publication_date

    @staticmethod
    def resolve_is_visible(root: models.GaduurPackage, _info):
        return root.is_published

class PackageLine(CountableDjangoObjectType):
    class Meta:
        description = "Represents line of the fulfillment."
        interfaces = [relay.Node]
        model = models.PackageLine
        only_fields = ["id", "name", "quantity", "currency", "unit_price_amount", "fulfillmentline"]



class Package(CountableDjangoObjectType):
    lines = graphene.List(
        PackageLine, description="List of lines for the fulfillment."
    )
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
            "perkg_amount",
            "net_or_gross",
            "perkg_price",
            "get_total",
            "created",
            "lines"
        ]
        interfaces = [relay.Node]
        model = models.Package

    def resolve_lines(root: models.Package, _info):
        return root.lines.all()
