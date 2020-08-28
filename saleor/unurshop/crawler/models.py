from django.db import models
from ...core.models import PublishableModel, PublishedQuerySet
from draftjs_sanitizer import clean_draft_js
from ...core.db.fields import SanitizedJSONField
from ..ushop.models import Shop

DEFAULT_SHOP_ID = 1


class Crawler(PublishableModel):
    url = models.URLField(max_length=200, unique=True)
    completed = models.BooleanField(default=False)
    crawled_at = models.DateTimeField(auto_now=True, null=True)
    product_count = models.PositiveSmallIntegerField(null=True, blank=True)
    # jsonData = models.TextField(blank=True)
    json_data = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_draft_js
    )
    json_data_backup = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_draft_js
    )

    shop = models.ForeignKey(Shop, related_name="crawlers",
                             on_delete=models.CASCADE, default=DEFAULT_SHOP_ID)
    listSelection = models.TextField(blank=True)
    productSelection = models.TextField(blank=True)

