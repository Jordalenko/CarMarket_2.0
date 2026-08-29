from decimal import Decimal
from datetime import timedelta
from uuid import UUID

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from listings.models import Listing
from users.models import Notification, Profile

from .models import Purchase, PurchaseItem


DELIVERY_THRESHOLD = Decimal("20000.00")
DELIVERY_FEE = Decimal("100.00")
RESERVATION_DURATION = timedelta(minutes=30)


def _selected_listing_ids(request):
    selected_ids = []
    for value in request.session.get("selected_vehicle_ids", []):
        try:
            selected_ids.append(str(UUID(str(value))))
        except (TypeError, ValueError, AttributeError):
            continue
    return selected_ids


def _calculate_totals(listings):
    vehicle_total = sum(
        (Decimal(listing.price or 0) for listing in listings),
        Decimal("0.00"),
    )
    delivery_fee = (
        DELIVERY_FEE
        if listings and vehicle_total < DELIVERY_THRESHOLD
        else Decimal("0.00")
    )
    return vehicle_total, delivery_fee


def _checkout_context(listings):
    vehicle_total, delivery_fee = _calculate_totals(listings)
    return {
        "selected_listings": listings,
        "vehicle_total": vehicle_total,
        "delivery_fee": delivery_fee,
        "checkout_total": vehicle_total + delivery_fee,
    }


def _available_listing_filter(now):
    return Q(checkout_reserved_until__isnull=True) | Q(
        checkout_reserved_until__lte=now,
    )


def _ensure_purchase_notification(purchase):
    profile, _ = Profile.objects.get_or_create(
        user=purchase.buyer,
        defaults={
            "username": purchase.buyer.username,
            "email": purchase.buyer.email,
            "name": purchase.buyer.get_full_name(),
        },
    )
    Notification.objects.get_or_create(
        profile=profile,
        subject="Purchase confirmed",
        message=(
            f"Your purchase {purchase.purchase_reference} is confirmed. "
            f"Total paid: €{purchase.total:,.2f}."
        ),
    )


def _ensure_sale_notification(purchase, subject, message):
    profile, _ = Profile.objects.get_or_create(
        user=purchase.buyer,
        defaults={
            "username": purchase.buyer.username,
            "email": purchase.buyer.email,
            "name": purchase.buyer.get_full_name(),
        },
    )
    Notification.objects.get_or_create(
        profile=profile,
        subject=subject,
        message=message,
    )


def _notify_admins(subject, message):
    admin_profiles = Profile.objects.filter(
        user__isnull=False,
    ).filter(
        user__is_staff=True,
    )
    for profile in admin_profiles:
        Notification.objects.get_or_create(
            profile=profile,
            subject=subject,
            message=message,
        )


def _finalize_paid_purchase(purchase, session):
    with transaction.atomic():
        purchase = Purchase.objects.select_for_update().get(pk=purchase.pk)
        if purchase.payment_status == Purchase.Status.PAID:
            return purchase

        purchase.stripe_checkout_session_id = session.get("id")
        purchase.stripe_payment_intent_id = session.get("payment_intent")
        purchase.payment_status = Purchase.Status.PAID
        purchase.completed_at = timezone.now()
        purchase.save(update_fields=[
            "stripe_checkout_session_id",
            "stripe_payment_intent_id",
            "payment_status",
            "completed_at",
        ])
        for item in PurchaseItem.objects.select_related("listing").filter(
            purchase=purchase,
        ):
            item.listing.is_sold = True
            item.listing.checkout_reserved_until = None
            item.listing.save(update_fields=["is_sold", "checkout_reserved_until"])
        _ensure_purchase_notification(purchase)
        _notify_admins(
            "Sale requires approval",
            f"Purchase {purchase.purchase_reference} has been paid and requires sale review.",
        )
        return purchase


@login_required(login_url="login")
def checkout_page(request):
    selected_ids = _selected_listing_ids(request)
    now = timezone.now()
    listings = list(
        Listing.objects.select_related("car_make", "car_model").filter(
            id__in=selected_ids,
            is_approved=True,
            is_sold=False,
        ).filter(_available_listing_filter(now))
    )
    listings_by_id = {str(listing.id): listing for listing in listings}
    ordered_listings = [
        listings_by_id[listing_id]
        for listing_id in selected_ids
        if listing_id in listings_by_id
    ]
    return render(
        request,
        "checkout/checkout.html",
        _checkout_context(ordered_listings),
    )


@require_http_methods(["POST"])
@login_required(login_url="login")
def create_checkout_session(request):
    selected_ids = _selected_listing_ids(request)
    if not selected_ids:
        messages.error(request, "Your checkout is empty.")
        return redirect("checkout:checkout_page")

    billing_name = (request.POST.get("billing_name") or "").strip()
    billing_email = (request.POST.get("billing_email") or "").strip()
    billing_phone = (request.POST.get("billing_phone") or "").strip()
    billing_address = (request.POST.get("billing_address") or "").strip()
    delivery_address = (request.POST.get("delivery_address") or "").strip()
    notes = (request.POST.get("notes") or "").strip()
    if not all((billing_name, billing_email, billing_phone, billing_address, delivery_address)):
        messages.error(request, "Please complete all required checkout details.")
        return redirect("checkout:checkout_page")

    now = timezone.now()
    reservation_until = now + RESERVATION_DURATION
    purchase = None
    listings = []
    with transaction.atomic():
        locked = list(
            Listing.objects.select_for_update()
            .filter(id__in=selected_ids, is_approved=True, is_sold=False)
        )
        by_id = {str(listing.id): listing for listing in locked}
        if len(by_id) != len(set(selected_ids)) or any(
            listing.checkout_reserved_until and listing.checkout_reserved_until > now
            for listing in locked
        ):
            messages.error(request, "One or more selected vehicles is no longer available.")
            return redirect("checkout:checkout_page")

        listings = [by_id[listing_id] for listing_id in selected_ids]
        vehicle_total, delivery_fee = _calculate_totals(listings)
        purchase = Purchase.objects.create(
            buyer=request.user,
            vehicle_total=vehicle_total,
            delivery_fee=delivery_fee,
            currency="EUR",
            billing_name=billing_name,
            billing_email=billing_email,
            billing_phone=billing_phone,
            billing_address=billing_address,
            delivery_address=delivery_address,
            notes=notes,
        )
        PurchaseItem.objects.bulk_create([
            PurchaseItem(
                purchase=purchase,
                listing=listing,
                agreed_price=Decimal(listing.price or 0),
            )
            for listing in listings
        ])
        Listing.objects.filter(id__in=selected_ids).update(
            checkout_reserved_until=reservation_until,
        )

    stripe.api_key = settings.STRIPE_SECRET_KEY
    line_items = [
        {
            "price_data": {
                "currency": "eur",
                "product_data": {"name": f"{listing.car_make} {listing.car_model}"},
                "unit_amount": int(Decimal(listing.price or 0) * 100),
            },
            "quantity": 1,
        }
        for listing in listings
    ]
    if purchase.delivery_fee:
        line_items.append({
            "price_data": {
                "currency": "eur",
                "product_data": {"name": "Worldwide delivery"},
                "unit_amount": int(purchase.delivery_fee * 100),
            },
            "quantity": 1,
        })

    try:
        site_url = f"{request.scheme}://{request.get_host()}"
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=line_items,
            customer_email=billing_email,
            success_url=(
                f"{site_url}/checkout/success/"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=f"{site_url}/checkout/cancel/",
            metadata={
                "purchase_id": str(purchase.id),
                "purchase_reference": purchase.purchase_reference,
            },
        )
    except stripe.error.StripeError:
        Purchase.objects.filter(pk=purchase.pk).update(
            payment_status=Purchase.Status.FAILED,
        )
        Listing.objects.filter(id__in=selected_ids).update(
            checkout_reserved_until=None,
        )
        messages.error(request, "Unable to start secure payment. Please try again.")
        return redirect("checkout:checkout_page")

    Purchase.objects.filter(pk=purchase.pk).update(
        stripe_checkout_session_id=session.id,
    )
    return redirect(session.url)


@require_http_methods(["GET"])
@login_required(login_url="login")
def checkout_success(request):
    purchase = get_object_or_404(
        Purchase,
        stripe_checkout_session_id=request.GET.get("session_id"),
        buyer=request.user,
    )
    if purchase.payment_status != Purchase.Status.PAID:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            session = stripe.checkout.Session.retrieve(
                request.GET.get("session_id")
            )
        except stripe.error.StripeError:
            session = None
        if (
            session
            and session.get("payment_status") == "paid"
            and session.get("metadata", {}).get("purchase_id") == str(purchase.id)
        ):
            purchase = _finalize_paid_purchase(purchase, session)
    if purchase.payment_status == Purchase.Status.PAID:
        _ensure_purchase_notification(purchase)
    request.session["selected_vehicle_ids"] = []
    request.session.modified = True
    return render(
        request,
        "checkout/success.html",
        {"purchase": purchase, "purchase_items": purchase.items.select_related(
            "listing__car_make", "listing__car_model"
        )},
    )


@require_http_methods(["GET"])
@login_required(login_url="login")
def checkout_cancel(request):
    return render(request, "checkout/cancel.html")


@require_http_methods(["GET"])
@login_required(login_url="login")
def purchase_history(request):
    purchases = Purchase.objects.filter(buyer=request.user).prefetch_related(
        "items__listing__car_make",
        "items__listing__car_model",
    )
    return render(request, "checkout/purchases.html", {"purchases": purchases})


@require_http_methods(["GET", "POST"])
@login_required(login_url="login")
def sale_reviews(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect("checkout:purchase_history")

    if request.method == "POST":
        purchase = get_object_or_404(
            Purchase,
            pk=request.POST.get("purchase_id"),
            payment_status=Purchase.Status.PAID,
            sale_status=Purchase.SaleStatus.PENDING_REVIEW,
        )
        action = (request.POST.get("action") or "").strip().lower()
        if action == "approve":
            purchase.sale_status = Purchase.SaleStatus.APPROVED
            purchase.save(update_fields=["sale_status"])
            _ensure_sale_notification(
                purchase,
                "Sale approved",
                f"Your purchase {purchase.purchase_reference} has been approved.",
            )
        elif action == "reject":
            purchase.sale_status = Purchase.SaleStatus.REJECTED
            purchase.save(update_fields=["sale_status"])
            for item in purchase.items.select_related("listing"):
                item.listing.is_sold = False
                item.listing.checkout_reserved_until = None
                item.listing.save(update_fields=["is_sold", "checkout_reserved_until"])
            _ensure_sale_notification(
                purchase,
                "Sale rejected",
                f"Your purchase {purchase.purchase_reference} was rejected and the vehicle(s) were relisted. A refund must be arranged by the administrator.",
            )
        return redirect("checkout:sale_reviews")

    purchases = Purchase.objects.filter(
        payment_status=Purchase.Status.PAID,
        sale_status=Purchase.SaleStatus.PENDING_REVIEW,
    ).prefetch_related("items__listing__car_make", "items__listing__car_model")
    return render(request, "checkout/sale_reviews.html", {"purchases": purchases})


@csrf_exempt
@require_http_methods(["POST"])
def stripe_webhook(request):
    if not settings.STRIPE_WH_SECRET:
        return HttpResponse("Webhook secret is not configured.", status=503)
    signature = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            signature,
            settings.STRIPE_WH_SECRET,
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponseBadRequest("Invalid webhook payload.")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            purchase_id = session.get("metadata", {}).get("purchase_id")
            purchase = Purchase.objects.filter(pk=purchase_id).first()
            if purchase:
                _finalize_paid_purchase(purchase, session)
    return HttpResponse(status=200)