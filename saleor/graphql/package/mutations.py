import graphene
from django.utils.text import slugify
from django.db import transaction

from .types import Gaduur, Package
from ..core.types import SeoInput, Upload
from ..core.types.common import SeoInput
from ..core.utils import validate_image_file
from ..core.scalars import Decimal
from ..account.types import AddressInput

from ..core.mutations import (  # ClearMetaBaseMutation,; UpdateMetaBaseMutation,
    BaseMutation,
    ModelDeleteMutation,
    ModelMutation,
)
from ...unurshop.package import models
from ...order.models import FulfillmentLine
from ...order import FulfillmentUshopStatus

class GaduurInput(graphene.InputObjectType):
    name = graphene.String(description="Gaduur name.")
    shipping_type = graphene.String(description="shipping type")
    is_published = graphene.Boolean(
        description="Determines if Gaduur is visible in the storefront"
    )
    publication_date = graphene.String(
        description="Publication date. ISO 8601 standard."
    )
    status = graphene.String(description="gaduur package status")
    start_date = graphene.String(description="teeverlesen ognoo")
    end_date = graphene.String(description="mongold ochih hugatss uridchilsan baidlaar")
    received_date = graphene.String(description="mongold ochson ognoo")
    tracking_number = graphene.String(description="teeveriin track code")


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




class PackageLineInput(graphene.InputObjectType):
    name = graphene.String(description="package line name")
    quantity = graphene.Int(required=True, description="quantity ")
    unit_price_amount = Decimal(required=True,description="line dahi negjin une")
    fulfillmentline_id = graphene.ID(description="fulfillmentLine id")


class PackageInput(graphene.InputObjectType): #AddressInput
    name = graphene.String(desciption="Package number")
    lines = graphene.List(PackageLineInput, description="package lines")
    shipping_address_id = graphene.ID(description="shipping address id")
    sender_address_id = graphene.ID(description="sender address id")
    width = Decimal(description="urgun")
    height = Decimal(description="under")
    length = Decimal(description="urt")
    net_weight = Decimal(description="бодит жин")
    gross_weight = Decimal(description="оврийн жин")
    perkg_amount = Decimal(description="Тээврийн үнэ")
    net_or_gross = graphene.String(description="net or gross")
    gaduur = graphene.ID(description="gaduur")


class PackageCreate(ModelMutation):
    class Arguments:
        input = PackageInput()

    class Meta:
        description = "Create a new package"
        model = models.Package
        permissions=("page.manage_pages")

    # @classmethod
    # def clean_input(cls, info, instance, data):
    #     cleaned_input = super().clean_input(info, instance, data)
    #     return cleaned_input

    @classmethod
    def save_lines (cls, instance: models.Package, cleaned_input: dict):
        lines = cleaned_input.get("lines", [])
        fulfillments = []

        for line in lines:
            _type, fullfillment_pk = graphene.Node.from_global_id(line.get("fulfillmentline_id"))
            packageLine = instance.lines.create(
                name=line.get("name"),
                quantity=line.get("quantity"),
                unit_price_amount=line.get("unit_price_amount"),
                fulfillmentline_id=fullfillment_pk
            )
            fline = FulfillmentLine.objects.get(pk=fullfillment_pk)
            fline.ushop_status = FulfillmentUshopStatus.SHIPPING
            fline.save()
            try:
                index = fulfillments.index(fline.fulfillment)
            except:
                fulfillments.append(fline.fulfillment)

        for fulfillment in fulfillments:
            status = fulfillment.get_line_status()
            if status != "diff":
                fulfillment.ushop_status = status
                fulfillment.save()

        if len(fulfillments) > 0:
            instance.sender_address = fulfillments[0].order.shipping_address
            instance.shipping_address = fulfillments[0].order.shipping_address
            instance.save()

    @classmethod
    @transaction.atomic()
    def save(cls, info, instance: models.Package, cleaned_input):
        instance.save()
        cls.save_lines(instance, cleaned_input)
        instance.gaduur.calc_and_save()

    # @classmethod
    # def clean_input(cls, info, instace: models.Package, data, input_cls=None):
    #     cleaned_input = super().clean_input(info, instance, data)
    #     user = info.context.user
    #     lines = data.pop("lines", None)

    #     if lines:
    #         for line in lines:

    # @classmethod
    # def perform_mutation(cls, _root, info, **data):
    #     user = info.context.user

    #     package = models.Package()

    #     package = cls.construct_instance(package, cleaned_input)
    #     cls.clean_instance(info, package)
    #     cls.save(info, package, cleaned_input)

    #     return PackageCreate(package=package, created=Trye)

class PackageUpdate(PackageCreate):
    class Arguments:
        id = graphene.ID(required=True, description="package id")
        input = PackageInput(
            required=True, description="fields required to update a package"
        )

    class Meta:
        description = "updates an existing package"
        model = models.Package
        permissions=("page.manage_pages")

class PackageDelete(ModelDeleteMutation):
    class Arguments:
        id = graphene.ID(required=True, description="id of package to delete")

    class Meta:
        description="delete package"
        model = models.Package
        permissions=("page.manage_pages")
