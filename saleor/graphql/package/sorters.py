import graphene

from ..core.types import SortInputObjectType

#############################
#### GADUUR
class GaduurSortField(graphene.Enum):
    NAME = ["name"]
    SHIPPING_TYPE = ["shipping_type"]
    VISIBILITY = ["is_published", "name", "shipping_type"]
    PUBLICATION_DATE = ["publication_date", "name", "shipping_type"]

    @property
    def description(self):
        if self.name in GaduurSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort gaduur by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class GaduurSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = GaduurSortField
        type_name = "gaduur"

class PackageSortField(graphene.Enum):
    NAME = ["name"]

    @property
    def description(self):
        if self.name in PackageSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort package by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)

class PackageSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = PackageSortField
        type_name="package"
