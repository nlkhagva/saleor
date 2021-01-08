import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import GaduurBulkDelete, PackageBulkDelete
from .mutations import GaduurCreate, GaduurDelete, GaduurUpdate, PackageCreate, PackageDelete, PackageUpdate
from .resolvers import resolve_gaduur, resolve_gaduurs, resolve_package, resolve_packages
from .sorters import GaduurSortingInput, PackageSortingInput
from .types import Gaduur, Package
from .filters import GaduurFilterInput, PackageFilterInput
from ..account.types import Address
from ..order.types import FulfillmentLine
from ..core.connection import CountableDjangoObjectType
from ...order.models import FulfillmentLine as FulfillmentLineModel

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
# class FlineCustom(CountableDjangoObjectType):
#     order_id = graphene.Int()
#     checked = graphene.Boolean()

#     class Meta:
#         description = "Represents line of the fulfillment."
#         interfaces = [graphene.relay.Node]
#         model = FulfillmentLineModel
#         only_fields = ["id", "quantity", "ustatus", "changed_date", "soon_date"]

#     @staticmethod
#     def resolve_order_id(root: FulfillmentLineModel, _info):
#         return root.order_line.order_id

#     def resoleve_checked(root: FulfillmentLineModel, _info):
#         return False

# class FlinesByAddress(graphene.ObjectType):
#     address = graphene.Field(
#        Address,
#        description="Хүлээн авах хаяг"
#     )
#     lines = graphene.List(
#        FlineCustom,
#        description="custom fulfillmentline"
#     )


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
    # flines_by_address = graphene.Field(
    #     FlinesByAddress,
    #     description="flines"
    # )

    def resolve_package(self, info, id=None):
        return resolve_package(info, id)
    def resolve_packages(self, info, query=None, **_kwargs):
        return resolve_packages(info, query=query)

    # def resolve_flines_by_address(self, info, ordernumber=None, **_kwargs):
    #     return resolve_flines_by_address(info, ordernumber)

class PackageMutations(graphene.ObjectType):
    package_create = PackageCreate.Field()
    package_delete = PackageDelete.Field()
    package_bulk_delete = PackageBulkDelete.Field()
    package_update = PackageUpdate.Field()
