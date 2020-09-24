import graphene
import tldextract

from ...unurshop.crawler import models
from ..core.mutations import (
    BaseMutation,
    ModelDeleteMutation,
    ModelMutation,
)
from .types import Crawler

class CrawlerInput(graphene.InputObjectType):
    url = graphene.String(description="crawler url")
    completed = graphene.Boolean(description="crawler duussan esegiig iltgene")
    product_count = graphene.Int(description="crawled product count")
    json_data = graphene.JSONString(description="crawled data")
    productSelection = graphene.String(description="product selection")
    listSelection = graphene.String(description="list selection")


class CrawlerCreate(ModelMutation):
    class Arguments:
        input = CrawlerInput(
            required=True, description="fields required to create a crawler"
        )

    class Meta:
        description = "create a new crawler"
        model = models.Crawler
        permissions = ("page.manage_pages",)

    @classmethod
    def clean_input(cls, info, instance, data, input_cls=None):
        cleaned_input = super().clean_input(info, instance, data, input_cls=input_cls)
        try:
            url = cleaned_input.get("url", "")
            domain = tldextract.extract(url).domain
            ushop = models.Shop.objects.filter(url__contains=domain)[0]
        except:
            # todorhoigui delguur
            ushop = models.Shop.objects.get(pk=1)

        cleaned_input["shop"] = ushop
        cleaned_input["listSelection"] = cleaned_input["listSelection"] if cleaned_input["listSelection"] else ushop.listSelection
        cleaned_input["productSelection"] = cleaned_input["productSelection"] if cleaned_input["productSelection"] else ushop.productSelection

        return cleaned_input

    @classmethod
    def get_type_for_model(cls):
        return Crawler

    # @classmethod
    # def perform_mutation(cls, root, info, **data):
    #     # ushop_id = data.pop("shop_id", None)

    #     # _type, shop_pk = graphene.Node.from_global_id(ushop_id)

    #     # data["input"]["shop_id"] = shop_pk
    #     return super().perform_mutation(root, info, **data)


class CrawlerUpdate(CrawlerCreate):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a crawler to update.")
        input = CrawlerInput(
            required=True, description="fields required to update a crawler info"
        )

    class Meta:
        description = "updates an existing crawler"
        model = models.Crawler
        permissions = ("page.manage_pages", )


class CrawlerDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True)

    class Meta:
        description = "deletes a crawler"
        model = models.Crawler
        permissions = ("page.manage_pages", )

    @classmethod
    def get_type_for_model(cls):
        return Crawler

