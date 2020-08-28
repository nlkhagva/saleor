import graphene
from django.utils.text import slugify

from .types import Gaduur
from ..core.types import SeoInput, Upload
from ..core.types.common import SeoInput
from ..core.utils import clean_seo_fields, validate_image_file

from ..core.mutations import (  # ClearMetaBaseMutation,; UpdateMetaBaseMutation,
    BaseMutation,
    ModelDeleteMutation,
    ModelMutation,
)
from ...unurshop.package import models


class GaduurInput(graphene.InputObjectType):
    name = graphene.String(description="Gaduur name.")
    is_published = graphene.Boolean(
        description="Determines if Gaduur is visible in the storefront"
    )
    publication_date = graphene.String(
        description="Publication date. ISO 8601 standard."
    )


class GaduurCreate(ModelMutation):
    class Arguments:
        input = GaduurInput(
            required=True, description="Fields required to create a Gaduur."
        )

    class Meta:
        description = "Creates a new Gaduur."
        model = models.GaduurPackage
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


class GaduurUpdate(GaduurCreate):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a Gaduur to update.")
        input = GaduurInput(
            required=True, description="Fields required to update a Gaduur."
        )

    class Meta:
        description = "Updates an existing Gaduur."
        model = models.GaduurPackage
        permissions = ("page.manage_pages",)


class GaduurDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="ID of a Gaduur to delete.")

    class Meta:
        description = "Deletes a Gaduur."
        model = models.GaduurPackage
        permissions = ("page.manage_pages",)
