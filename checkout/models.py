import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models

from listings.models import Listing


def generate_purchase_reference():
    return uuid.uuid4().hex[:12].upper()


class Purchase(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    class SaleStatus(models.TextChoices):
        PENDING_REVIEW = "pending_review", "Pending admin review"
        APPROVED = "approved", "Sale approved"
        REJECTED = "rejected", "Sale rejected"
        CANCELLED = "cancelled", "Sale cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase_reference = models.CharField(
        max_length=12,
        unique=True,
        editable=False,
        default=generate_purchase_reference,
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="vehicle_purchases",
    )
    stripe_checkout_session_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    stripe_payment_intent_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    vehicle_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    delivery_fee = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    currency = models.CharField(max_length=3, default="EUR")
    payment_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    sale_status = models.CharField(
        max_length=20,
        choices=SaleStatus.choices,
        default=SaleStatus.PENDING_REVIEW,
    )
    billing_name = models.CharField(max_length=255)
    billing_email = models.EmailField()
    billing_phone = models.CharField(max_length=50, blank=True)
    billing_address = models.TextField()
    delivery_address = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.purchase_reference

    @property
    def total(self):
        return self.vehicle_total + self.delivery_fee


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name="items",
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.PROTECT,
        related_name="purchase_items",
    )
    agreed_price = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["purchase", "listing"],
                name="unique_listing_per_purchase",
            ),
        ]

    def __str__(self):
        return f"{self.purchase} - {self.listing}"