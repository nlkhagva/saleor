from django.db import models

# Create your models here.

from django.conf import settings
from django.db import models
from django_prices.models import MoneyField
from versatileimagefield.fields import PPOIField, VersatileImageField
from django.contrib.postgres.fields import JSONField
from draftjs_sanitizer import clean_draft_js

from ..seo.models import SeoModel, SeoModelTranslation
from ..core.models import PublishableModel, PublishedQuerySet
from ..core.db.fields import SanitizedJSONField

DEFAULT_SHOP_ID = 1

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


class GaduurPackage(PublishableModel):
    name = models.TextField(max_length=20, unique=True)
    shipping_type = models.PositiveSmallIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

#     total_weight = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     actual_weight = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     cargo_total_weight = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     cargo_total_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     cargo_paid_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     cargo_remain_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     zahialga_total_weight = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     zahialga_total_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     zahialga_paid_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     zahialga_remain_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     uuruu_total_weight = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     uuruu_total_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     uuruu_paid_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     uuruu_remain_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     total_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     total_paid_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     total_remain_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     total_cost = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     total_income = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
#     tracking_number = models.TextField(max_length=50, null=True, blank=True)
#     package_count = models.IntegerField(null=True, blank=True)
#     received_count = models.IntegerField(null=True, blank=True)
#     hot_count = models.IntegerField(null=True, blank=True)
#     huduu_count = models.IntegerField(null=True, blank=True)
class Package:
    pass 
