import graphene

from ...unurshop.ushop import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation


class UshopBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of ushop IDs to delete."
        )

    class Meta:
        description = "Deletes shops."
        model = models.Shop
        permissions = ("page.manage_pages",)


class UshopBulkPublish(BaseBulkMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of ushop IDs to (un)publish."
        )
        is_published = graphene.Boolean(
            required=True, description="Determine if ushops will be published or not."
        )

    class Meta:
        description = "Publish ushops."
        model = models.Shop
        permissions = ("page.manage_pages",)

    @classmethod
    def bulk_action(cls, queryset, is_published):
        queryset.update(is_published=is_published)
