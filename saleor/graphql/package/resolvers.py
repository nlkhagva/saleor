import graphene

from ...unurshop.package import models
from ...order.models import Fulfillment as FModel, FulfillmentLine as FlineModel, Order as OrderModel
from .types import Gaduur, Package
import tldextract
from django.db.models import Q

USHOP_SEARCH_FIELDS = ("description", "name", "url")


def resolve_gaduur(info, gaduur_id=None):
    assert gaduur_id, "No gaduur ID provided."
    user = info.context.user

    gaduur = graphene.Node.get_node_from_global_id(info, gaduur_id, Gaduur)
    # Resolve to null if page is not published and user has no permission
    # to manage pages.
    is_available_to_user = (
        gaduur and gaduur.is_published or user.has_perm("page.manage_pages")
    )
    if not is_available_to_user:
        gaduur = None

    return gaduur


def resolve_gaduurs(info, query):
    user = info.context.user
    return models.GaduurPackage.objects.visible_to_user(user)


def resolve_package(info, global_id = None):
    assert global_id, "no id "
    user = info.context.user

    package = graphene.Node.get_node_from_global_id(info, global_id, Package)

    return package

def resolve_packages(info, query):
    return models.Package.objects.all()


def resolve_new_gaduurs(info):
    return models.GaduurPackage.objects.filter(status="new")


def resolve_flines_by_address(info, ordernumber):
    fs = FModel.objects.get(tracking_number=ordernumber)

    allorder = FlineModel.objects.filter(order_line__order_id = fs.order.id).filter(fulfillments)

    pass
