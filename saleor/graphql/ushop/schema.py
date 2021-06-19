import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import UshopBulkDelete, UshopBulkPublish
from .mutations import UshopCreate, UshopDelete, UshopUpdate
from .resolvers import resolve_ushop, resolve_ushopByLink, resolve_ushops, resolve_ushopSkuNext
from .sorters import UshopSortingInput
from .types import Ushop, SkuNext
from .filters import UshopFilterInput


class UshopQueries(graphene.ObjectType):
    ushop = graphene.Field(
        Ushop,
        id=graphene.Argument(graphene.ID),
        description="Lookup a page by ID.",
    )
    ushopByLink = graphene.Field(
        Ushop,
        link=graphene.String()
    )

    ushops = FilterInputConnectionField(
        Ushop,
        sort_by=UshopSortingInput(description="Sort ushops."),
        filter=UshopFilterInput(description="Filtering options for ushop."),
        description="List of the ushop's.",
    )
    ushopSkuNext = graphene.Field(
        SkuNext,
        description="facebook live next SKU Code"
    )

    def resolve_ushop(self, info, id=None):
        return resolve_ushop(info, id)

    def resolve_ushopByLink(self, info, link=None):
        return resolve_ushopByLink(info, link)

    def resolve_ushops(self, info, query=None, **_kwargs):
        return resolve_ushops(info, query=query)
    
    def resolve_ushopSkuNext(self, info, **data):
        return resolve_ushopSkuNext(info, data)


class UshopMutations(graphene.ObjectType):
    ushop_create = UshopCreate.Field()
    ushop_delete = UshopDelete.Field()
    ushop_bulk_delete = UshopBulkDelete.Field()
    ushop_bulk_publish = UshopBulkPublish.Field()
    ushop_update = UshopUpdate.Field()
