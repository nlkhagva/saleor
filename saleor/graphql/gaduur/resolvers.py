import graphene

from ...unurshop import models
from .types import Gaduur
import tldextract

USHOP_SEARCH_FIELDS = ("description", "name", "url")


def resolve_gaduur(info, gaduur_id=None):
    assert gaduur_id, "No gaduur ID or slug provided."
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
