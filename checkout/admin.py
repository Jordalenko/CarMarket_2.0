from django.contrib import admin

from .models import Purchase, PurchaseItem


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 0


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "purchase_reference",
        "buyer",
        "vehicle_total",
        "delivery_fee",
        "currency",
        "payment_status",
        "sale_status",
        "created_at",
        "completed_at",
    )
    list_filter = ("payment_status", "sale_status", "currency", "created_at")
    search_fields = (
        "purchase_reference",
        "buyer__username",
        "stripe_checkout_session_id",
        "stripe_payment_intent_id",
    )
    inlines = [PurchaseItemInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        if form.instance.sale_status == Purchase.SaleStatus.APPROVED:
            for item in form.instance.items.select_related("listing"):
                item.listing.is_sold = True
                item.listing.checkout_reserved_until = None
                item.listing.save(
                    update_fields=["is_sold", "checkout_reserved_until"]
                )
        elif form.instance.sale_status == Purchase.SaleStatus.REJECTED:
            for item in form.instance.items.select_related("listing"):
                item.listing.is_sold = False
                item.listing.checkout_reserved_until = None
                item.listing.save(
                    update_fields=["is_sold", "checkout_reserved_until"]
                )