import graphene

from ...unurshop.crawler import models
from .types import Crawler
import tldextract

CRAWLER_SEARCH_FIELDS = ("url", "shop", "completed")


def resolve_crawler(info, crawler_id=None):
    assert crawler_id, "No crawler ID or slug provided."
    user = info.context.user

    crawler = graphene.Node.get_node_from_global_id(info, crawler_id, Crawler)
    # Resolve to null if page is not published and user has no permission
    # to manage pages.

    return crawler


def resolve_crawlers(info, query):
    user = info.context.user
    return models.Crawler.objects.visible_to_user(user)
