from django.db import models
from django.conf import settings
from django_prices.models import MoneyField
from django.utils.timezone import now
# from versatileimagefield.fields import PPOIField, VersatileImageField
from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from draftjs_sanitizer import clean_draft_js
from ...core.db.fields import SanitizedJSONField
from functools import reduce

from ...seo.models import SeoModel, SeoModelTranslation
from ...core.models import PublishableModel, PublishedQuerySet

from ...account.models import Address
from ...order.models import FulfillmentLine

from . import PackageStatus, PackageNetOrGross, PackageType


class GaduurPackage(PublishableModel):
    name = models.TextField(max_length=20, unique=True)
    shipping_type = models.TextField(max_length=10, blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    received_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=32, default=PackageStatus.NEW, choices=PackageStatus.CHOICES)

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

    def calc_and_save(self):
        cal_sum = lambda a, b: a + b
        packages = self.packages.all()

        self.net_weight = reduce(cal_sum, [package.net_weight for package in packages], 0)
        self.gross_weight = reduce(cal_sum, [package.gross_weight for package in packages], 0)
        self.total_amount = reduce(cal_sum, [package.get_total_amount() for package in packages], 0)
        self.package_count = reduce(cal_sum, [len(packages)], 0)
        self.save()



class Package(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    name = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=32, default=PackageStatus.DRAFT, choices=PackageStatus.CHOICES,)
    package_type = models.CharField(max_length=32, default=PackageType.ORDER, choices=PackageType.CHOICES,)
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
    net_or_gross = models.CharField(
        max_length=16,
        default=PackageNetOrGross.NET,
        choices=PackageNetOrGross.CHOICES,
    )
    perkg_amount = models.DecimalField(
        max_digits=settings.DEFAULT_MAX_DIGITS,
        decimal_places=settings.DEFAULT_DECIMAL_PLACES,
        default=0,
    )
    perkg_price = MoneyField(
        amount_field="perkg_amount", currency_field="currency"
    )

    def get_customer_email(self):
        return self.user.email if self.user else self.user_email

    def get_total_amount(self):
        return self.perkg_amount * (self.net_weight if self.net_or_gross == PackageNetOrGross.NET else self.gross_weight)

    def update_gaduur_info(self):
        pass
        # self.gaduur.total


class PackageLine(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    package = models.ForeignKey(
        Package,
        related_name="lines",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    fulfillmentline = models.ForeignKey(
        FulfillmentLine,
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

