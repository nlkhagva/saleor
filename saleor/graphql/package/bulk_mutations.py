import graphene

from ...unurshop.package import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation


class GaduurBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of gaduur IDs to delete."
        )

    class Meta:
        description = "Deletes gad."
        model = models.GaduurPackage
        permissions = ("page.manage_pages",)


