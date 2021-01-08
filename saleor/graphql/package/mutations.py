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
from ...order.models import FulfillmentLine, OrderLine
from ...order.utils import add_variant_to_draft_order, recalculate_order
from ...unurshop.package import PackageStatus
from ...product.models import ProductVariant

class GaduurInput(graphene.InputObjectType):
    name = graphene.String(description="Gaduur name.")
    shipping_type = graphene.String(description="shipping type")
    is_published = graphene.Boolean(
        description="Determines if Gaduur is visible in the storefront"
    )
    publication_date = graphene.String(
        description="Publication date. ISO 8601 standard."
    )
    ustatus = graphene.String(description="gaduur package status")
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
            fline.ustatus = PackageStatus.SHIPPING
            fline.save()
            try:
                index = fulfillments.index(fline.fulfillment)
            except:
                fulfillments.append(fline.fulfillment)

        for fulfillment in fulfillments:
            status = fulfillment.get_line_status()
            if status != "diff":
                fulfillment.ustatus = status
                fulfillment.save()

        if len(fulfillments) > 0:
            #zahialga der ilgeemjiin tulbur nemeh heseg
            mn_cargo = ProductVariant.objects.get(pk=404)
            weight = float(cleaned_input.get("net_weight", 0)) if cleaned_input.get("net_or_gross", "net") == "net" else float(cleaned_input.get("gross_weight", 0))
            perkg = float(cleaned_input.get("perkg_amount", 0))
            quantity = perkg*weight*100

            if not instance.order_line:
                order_line = add_variant_to_draft_order(fulfillments[0].order, mn_cargo, quantity)
                order_line.product_name = "#" + instance.name + " " + order_line.product_name
                order_line.save(update_fields=["product_name"])

                instance.order_line = order_line
                instance.save()
            else:
                order_line = instance.order_line
                order_line.quantity = quantity
                order_line.save(update_fields=["quantity"])

            recalculate_order(fulfillments[0].order)

            instance.user = fulfillments[0].order.user
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

    @classmethod
    @transaction.atomic()
    def clean_instance(cls, info, instance):
        fulfillments = []

        for line in instance.lines.all():
            if line.fulfillmentline:
                line.fulfillmentline.ustatus = PackageStatus.ATUK
                line.fulfillmentline.save()

                try:
                    index = fulfillments.index(line.fulfillmentline.fulfillment)
                except:
                    fulfillments.append(line.fulfillmentline.fulfillment)
                line.delete()

        for fulfillment in fulfillments:
            status = fulfillment.get_line_status()
            if status != "diff":
                fulfillment.ustatus = status
                fulfillment.save()

        if instance.order_line:
            order = instance.order_line.order
            instance.order_line.delete()

        recalculate_order(fulfillments[0].order)

