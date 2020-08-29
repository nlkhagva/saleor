import graphene

from ..core.types import SortInputObjectType


class GaduurSortField(graphene.Enum):
    TITLE = ["name"]
    VISIBILITY = ["is_published", "name", "url"]
    PUBLICATION_DATE = ["publication_date", "name", "url"]

    @property
    def description(self):
        if self.name in GaduurSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort ushops by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class GaduurSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = GaduurSortField
        type_name = "ushops"
