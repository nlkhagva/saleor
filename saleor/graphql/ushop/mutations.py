import graphene
from django.utils.text import slugify

from .types import Ushop
from ..core.types import SeoInput, Upload
from ..core.types.common import SeoInput
from ..core.utils import clean_seo_fields, validate_image_file

from ..core.mutations import (  # ClearMetaBaseMutation,; UpdateMetaBaseMutation,
    BaseMutation,
    ModelDeleteMutation,
    ModelMutation,
)
from ...unurshop.ushop import models
from ...unurshop.ushop.thumbnails import create_ushop_logo_image_thumbnails


class UshopInput(graphene.InputObjectType):
    name = graphene.String(description="Ushop name.")
    url = graphene.String(description="Ushop url.")
    description = graphene.String(
        description=("Ushop content. May consists of ordinary text, HTML and images.")
    )
    description_json = graphene.JSONString(description="Ushop content in JSON format.")
    is_published = graphene.Boolean(
        description="Determines if Ushop is visible in the storefront"
    )
    publication_date = graphene.String(
        description="Publication date. ISO 8601 standard."
    )
    seo = SeoInput(description="Search engine optimization fields.")
    logo_image = Upload(description="Logo image file.")
    logo_image_alt = graphene.String(description="Alt text for an image.")
    rank = graphene.Int(description="shop rank")
    rating_main = graphene.Int(description="main rank")
    rating_uk_shipping = graphene.Int(description="rating_uk_shipping rank")
    rating_product_quality = graphene.Int(description="rating_product_quality rank")
    rating_product_price = graphene.Int(description="marating_product_pricein rank")
    rating_shuurhai = graphene.Int(description="rating_shuurhai rank")
    rating_product_rank = graphene.Int(description="rating_product_rank rank")

    shipment_fee = graphene.Float(description="shipment_fee price")
    shipping_fee_yaraltai = graphene.Float(description="shipping_fee_yaraltai price")
    shipping_fee_free = graphene.Float(description="shipping_fee_free price")
    shipping_deliver_yaraltai = graphene.String(description="shipping_deliver_yaraltai")
    shipping_deliver_standart = graphene.String(description="shipping_deliver_standart")
    shipping_deliver_free = graphene.String(description="shipping_deliver_free")
    listSelection = graphene.String(
        description=("Ushop listiig zadlah selection")
    )
    productSelection = graphene.String(
        description=("Ushop productiig zadlah selection")
    )


class UshopCreate(ModelMutation):
    class Arguments:
        input = UshopInput(
            required=True, description="Fields required to create a Ushop."
        )

    class Meta:
        description = "Creates a new Ushop."
        model = models.Shop
        permissions = ("page.manage_pages",)

    @classmethod
    def clean_input(cls, info, instance, data):
        cleaned_input = super().clean_input(info, instance, data)
        # slug = cleaned_input.get("slug", "")
        # if not slug:
        #     cleaned_input["slug"] = slugify(cleaned_input["title"])
        if data.get("logo_image"):
            image_data = info.context.FILES.get(data["logo_image"])
            validate_image_file(image_data, "logo_image")

        clean_seo_fields(cleaned_input)
        return cleaned_input

    @classmethod
    def save(cls, info, instance, cleaned_input):
        instance.save()
        if cleaned_input.get("logo_image"):
            create_ushop_logo_image_thumbnails.delay(instance.pk)


class UshopUpdate(UshopCreate):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a Ushop to update.")
        input = UshopInput(
            required=True, description="Fields required to update a Ushop."
        )

    class Meta:
        description = "Updates an existing Ushop."
        model = models.Shop
        permissions = ("page.manage_pages",)


class UshopDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a Ushop to delete.")

    class Meta:
        description = "Deletes a Ushop."
        model = models.Shop
        permissions = ("page.manage_pages",)
