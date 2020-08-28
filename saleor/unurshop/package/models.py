from django.db import models
from django.conf import settings
from django_prices.models import MoneyField
from django.utils.timezone import now
# from versatileimagefield.fields import PPOIField, VersatileImageField
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from draftjs_sanitizer import clean_draft_js
from ...core.db.fields import SanitizedJSONField

from ...seo.models import SeoModel, SeoModelTranslation
from ...core.models import PublishableModel, PublishedQuerySet

from ...account.models import Address
from ...order.models import OrderLine

from . import PackageStatus


class GaduurPackage(PublishableModel):
    name = models.TextField(max_length=20, unique=True)
    shipping_type = models.PositiveSmallIntegerField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    total_weight = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
    actual_weight = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
    total_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
    total_paid_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
#     total_remain_amount = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
    total_cost = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
#     total_income = models.DecimalField(
#         max_digits=settings.DEFAULT_MAX_DIGITS,
#         decimal_places=settings.DEFAULT_DECIMAL_PLACES,
#         null=True,
#         blank=True
#     )
    tracking_number = models.TextField(max_length=50, null=True, blank=True)
    package_count = models.IntegerField(null=True, blank=True)
    received_count = models.IntegerField(null=True, blank=True)
    hot_count = models.IntegerField(null=True, blank=True)
    huduu_count = models.IntegerField(null=True, blank=True)


class Package(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    status = models.CharField(max_length=32, default=PackageStatus)
    gaduur = models.ForeignKey(
        GaduurPackage,
        null=True,
        blank=True,
        related_name="packages",
        on_delete=models.SET_NULL
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        related_name="packages",
        on_delete=models.SET_NULL
    )
    shipping_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    sender_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )

    upostPK = models.CharField(max_length=32, null=True, blank=True)

    net_weight = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
    gross_weight = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )

    width = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
    height = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )
    length = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )
    total_gross_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    total_gross = MoneyField(
        amount_field="total_gross_amount", currency_field="currency"
    )


class PackageLine(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    package = models.ForeignKey(
        Package,
        related_name="lines",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    order_line = models.ForeignKey(
        OrderLine,
        related_name="+",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    currency = models.CharField(
        max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH,
        default=settings.DEFAULT_CURRENCY,
    )

    unit_price_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
    )
    unit_price = MoneyField(
        amount_field="unit_price_amount", currency_field="currency"
    )

class BaraaNershil(models.Model):
    name = models.CharField(max_length=50)
    galig = models.CharField(max_length=250, null=True)

