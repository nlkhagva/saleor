import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import GaduurBulkDelete
from .mutations import GaduurCreate, GaduurDelete, GaduurUpdate
from .resolvers import resolve_gaduur, resolve_gaduurs
from .sorters import GaduurSortingInput
from .types import Gaduur
from .filters import GaduurFilterInput


class GaduurQueries(graphene.ObjectType):
    #####################
    ####  gaduur dagavar
    gaduur = graphene.Field(
        Gaduur,
        id=graphene.Argument(graphene.ID),
        description="Lookup a page by ID.",
    )
    gaduurs = FilterInputConnectionField(
        Gaduur,
        sort_by=GaduurSortingInput(description="Sort pages."),
        filter=GaduurFilterInput(description="Filtering options for pages."),
        description="List of the gaduur's.",
    )

    def resolve_gaduur(self, info, id=None):
        return resolve_gaduur(info, id)
    def resolve_gaduurs(self, info, query=None, **_kwargs):
        return resolve_gaduurs(info, query=query)




class GaduurMutations(graphene.ObjectType):
    gaduur_create = GaduurCreate.Field()
    gaduur_delete = GaduurDelete.Field()
    gaduur_bulk_delete = GaduurBulkDelete.Field()
    gaduur_update = GaduurUpdate.Field()
