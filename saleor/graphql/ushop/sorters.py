import graphene

from ..core.types import SortInputObjectType


class UshopSortField(graphene.Enum):
    TITLE = ["name"]
    SLUG = ["url"]
    VISIBILITY = ["is_published", "name", "url"]
    CREATION_DATE = ["updated_at", "name", "url"]
    PUBLICATION_DATE = ["publication_date", "name", "url"]

    @property
    def description(self):
        if self.name in UshopSortField.__enum__._member_names_:
            sort_name = self.name.lower().replace("_", " ")
            return f"Sort ushops by {sort_name}."
        raise ValueError("Unsupported enum value: %s" % self.value)


class UshopSortingInput(SortInputObjectType):
    class Meta:
        sort_enum = UshopSortField
        type_name = "ushops"
