import graphene

from ...unurshop.crawler import models
from ..core.mutations import BaseBulkMutation, ModelBulkDeleteMutation


class CrawlerBulkDelete(ModelBulkDeleteMutation):
    class Arguments:
        ids = graphene.List(
            graphene.ID, required=True, description="List of crawler IDs to delete."
        )

    class Meta:
        description = "Deletes pages."
        model = models.Crawler
        permissions = ("page.manage_pages",)


