import graphene

from ...unurshop.ushop import models
from ...product.models import ProductVariant
from .types import Ushop
import tldextract

USHOP_SEARCH_FIELDS = ("description", "name", "url")


def resolve_ushop(info, ushop_id=None):
    assert ushop_id, "No ushop ID or slug provided."
    user = info.context.user

    ushop = graphene.Node.get_node_from_global_id(info, ushop_id, Ushop)
    # Resolve to null if page is not published and user has no permission
    # to manage pages.
    is_available_to_user = (
        ushop and ushop.is_published or user.has_perm("page.manage_pages")
    )
    if not is_available_to_user:
        ushop = None

    return ushop


def resolve_ushopByLink(info, link=None):
    try:
        domain = tldextract.extract(link).domain
        ushop = models.Shop.objects.filter(url__contains=domain)[0]
    except:
        # todorhoigui delguur
        ushop = models.Shop.objects.get(pk=1)

    return ushop


def resolve_ushops(info, query):
    user = info.context.user
    return models.Shop.objects.visible_to_user(user)

def resolve_ushopSkuNext(info, data):
    variants = ProductVariant.objects.filter(sku__startswith='FB').order_by('-sku')
    if variants:
        sku =  variants[0].sku
        if sku:
            sku_int = int(sku[2:])
            sku_int += 1
            sku_str = str(sku_int)
            return {"sku" :"FB" + sku_str.zfill(4)}

    return {"sku":'FB0001'}