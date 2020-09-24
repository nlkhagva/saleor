import graphene

from ..core.fields import FilterInputConnectionField
from .bulk_mutations import CrawlerBulkDelete
from .filters import CrawlerFilterInput
from .mutations import CrawlerDelete
from .mutations import CrawlerCreate, CrawlerDelete, CrawlerUpdate
from .resolvers import resolve_crawler, resolve_crawlers
from .types import Crawler


class CrawlerQueries(graphene.ObjectType):
    crawler = graphene.Field(
        Crawler,
        id=graphene.Argument(graphene.ID, description="id of the crawler")
    )

    crawlers = FilterInputConnectionField(
        Crawler,
        filter=CrawlerFilterInput(description="filtering options for crawlers"),
        description="List of the crawlers pages"
    )

    def resolve_crawler(self, info, id=None):
        return resolve_crawler(info, id)

    def resolve_crawlers(self, info, query=None, **_kwargs):
        return resolve_crawlers(info, query=query)


class CrawlerMutations(graphene.ObjectType):
    crawler_create = CrawlerCreate.Field()
    crawler_delete = CrawlerDelete.Field()
    crawler_update = CrawlerUpdate.Field()
    crawler_bulk_delete = CrawlerBulkDelete.Field()
