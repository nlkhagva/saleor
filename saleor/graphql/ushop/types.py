import graphene
from graphene import relay

from ...unurshop.ushop import models

from ..core.connection import CountableDjangoObjectType
from ..core.types import (
    Image
)


class Ushop(CountableDjangoObjectType):
    available_on = graphene.Date(
        deprecation_reason="availableOn is deprecated, use publicationDate instead"
    )

    is_visible = graphene.Boolean(
        deprecation_reason="isVisible is deprecated, use isPublished instead"
    )

    # url = graphene.String(description="The online shop's URL for the category.")

    logo_image = graphene.Field(
        Image, size=graphene.Int(description="Size of the image")
    )

    class Meta:
        description = """A static page that can be manually added by a shop
               operator through the dashboard."""
        only_fields = [
            "id",
            "name",
            "url",
            "logo_image",
            "description",
            "description_json",
            "rank",
            "rating_main",
            "rating_uk_shipping",
            "rating_product_quality",
            "rating_product_price",
            "rating_shuurhai",
            "rating_product_rank",
            "shipping_product",
            # "has_shipping_tax",
            # "is_show_in_front",
            # "shipping_per_product",
            # "open_graph",
            # "autofill",
            # "xero_id",
            # "updated_at",
            "is_published",
            "publication_date",
            "seo_description",
            "seo_title",
            "listSelection",
            "productSelection",
        ]
        interfaces = [relay.Node]
        model = models.Shop

    @staticmethod
    def resolve_available_on(root: models.Shop, _info):
        return root.publication_date

    @staticmethod
    def resolve_is_visible(root: models.Shop, _info):
        return root.is_published

    @staticmethod
    def resolve_logo_image(root: models.Shop, info, size=None, **_kwargs):
        if root.logo_image:
            return Image.get_adjusted(
                image=root.logo_image,
                alt=root.logo_image_alt,
                size=size,
                rendition_key_set="logo_images",
                info=info,
            )
