import graphene

from ...unurshop.package import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation


class GaduurBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of gaduur IDs to delete."
        )

    class Meta:
        description = "Deletes gaduur."
        model = models.GaduurPackage
        permissions = ("page.manage_pages",)

class PackageBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="list of package IDs to delete"
        )
    class Meta:
        description="Delete packages"
        model = models.Package
        permissions = ("page.manage_pages")

