import graphene

from ...menu import models
from ..core.validators import validate_one_of_args_is_in_query
from ..utils.filters import filter_by_query_param
from .types import Menu

MENU_SEARCH_FIELDS = ("name",)
MENU_ITEM_SEARCH_FIELDS = ("name",)


def resolve_menu(info, menu_id=None, name=None):
    validate_one_of_args_is_in_query("id", menu_id, "name", name)
    if menu_id:
        return graphene.Node.get_node_from_global_id(info, menu_id, Menu)
    if name:
        return models.Menu.objects.filter(name=name).first()


def resolve_menus(info, query, **_kwargs):
    qs = models.Menu.objects.all()
    return filter_by_query_param(qs, query, MENU_SEARCH_FIELDS)


def resolve_menu_items(info, query, **_kwargs):
    qs = models.MenuItem.objects.all()
    return filter_by_query_param(qs, query, MENU_ITEM_SEARCH_FIELDS)

def resolve_mainmenu(info, data):
    women = models.Menu.objects.filter(name="women-navbar").first()
    men = models.Menu.objects.filter(name="men-navbar").first()
    kids = models.Menu.objects.filter(name="kids-navbar").first()

    return {"women": women, "men": men, "kids": kids}