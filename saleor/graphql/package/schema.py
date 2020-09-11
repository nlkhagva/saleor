import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import GaduurBulkDelete, PackageBulkDelete
from .mutations import GaduurCreate, GaduurDelete, GaduurUpdate, PackageCreate, PackageDelete, PackageUpdate
from .resolvers import resolve_gaduur, resolve_gaduurs, resolve_package, resolve_packages
from .sorters import GaduurSortingInput, PackageSortingInput
from .types import Gaduur, Package
from .filters import GaduurFilterInput, PackageFilterInput


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


###################################
# PACKAGES
class PackageQueries(graphene.ObjectType):
    package = graphene.Field(
        Package,
        id=graphene.Argument(graphene.ID),
        description="Look up a page by ID"
    )
    packages = FilterInputConnectionField(
        Package,
        sort_by=PackageSortingInput(description="sort packages"),
        filter=PackageFilterInput(description="filtering options for package"),
        description="List of the package"
    )

    def resolve_package(self, info, id=None):
        return resolve_package(info,id)
    def resolve_packages(self, info, query=None, **_kwargs):
        return resolve_packages(info, query=query)

class PackageMutations(graphene.ObjectType):
    package_create = PackageCreate.Field()
    package_delete = PackageDelete.Field()
    package_bulk_delete = PackageBulkDelete.Field()
    package_update = PackageUpdate.Field()
