from django.db import models
from versatileimagefield.fields import PPOIField, VersatileImageField
from ...core.db.fields import SanitizedJSONField
from draftjs_sanitizer import clean_draft_js
from ...seo.models import SeoModel, SeoModelTranslation
from ...core.models import PublishableModel, PublishedQuerySet

class Shop(SeoModel, PublishableModel):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    logo_image = VersatileImageField(
        upload_to="unurshop-shop", blank=True, null=True
    )
    logo_image_alt = models.CharField(max_length=128, blank=True)

    description = models.TextField(blank=True)
    description_json = SanitizedJSONField(
        blank=True, default=dict, sanitizer=clean_draft_js,
    )

    rank = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_main = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_uk_shipping = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_product_quality = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_product_price = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_shuurhai = models.PositiveSmallIntegerField(null=True, blank=True)
    rating_product_rank = models.PositiveSmallIntegerField(null=True, blank=True)

    has_shipping_tax = models.BooleanField(default=False, null=True, blank=True)
    shipping_per_product = models.BooleanField(default=False, null=True, blank=True)
    open_graph = models.BooleanField(default=False, null=True, blank=True)
    autofill = models.BooleanField(default=True, null=True, blank=True)
    xero_id = models.CharField(max_length=100, blank=True, default=0, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    listSelection = models.TextField(blank=True, null=True)
    productSelection = models.TextField(blank=True, null=True)

    shipping_product = models.ForeignKey(
        to="product.Product",
        related_name="shipping_product",
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
