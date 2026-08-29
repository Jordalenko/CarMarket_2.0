import uuid
from decimal import Decimal

from django.db.models import Q
from django.utils import timezone

from .models import Listing


SESSION_KEY_SELECTED_VEHICLES = "selected_vehicle_ids"
DELIVERY_THRESHOLD = Decimal("20000.00")
DELIVERY_FEE = Decimal("100.00")


def selected_vehicles(request):
    """Expose selected vehicles in session to all templates."""
    if not request.user.is_authenticated:
        return {
            "selected_vehicle_ids": [],
            "selected_vehicles": [],
            "selected_vehicle_count": 0,
            "selected_vehicle_subtotal": 0,
            "selected_vehicle_subtotal_display": "0",
            "selected_vehicle_delivery_fee": Decimal("0.00"),
            "selected_vehicle_total": Decimal("0.00"),
        }

    raw_ids = request.session.get(SESSION_KEY_SELECTED_VEHICLES, [])
    parsed_ids = []
    for value in raw_ids:
        try:
            parsed_ids.append(uuid.UUID(str(value)))
        except (TypeError, ValueError):
            continue

    vehicles_qs = Listing.objects.select_related("car_make", "car_model").filter(
        id__in=parsed_ids,
        is_approved=True,
        is_sold=False,
    ).filter(
        Q(checkout_reserved_until__isnull=True)
        | Q(checkout_reserved_until__lte=timezone.now())
    )
    vehicles_by_id = {vehicle.id: vehicle for vehicle in vehicles_qs}
    ordered_vehicles = [vehicles_by_id[_id] for _id in parsed_ids if _id in vehicles_by_id]
    subtotal = sum(vehicle.price or 0 for vehicle in ordered_vehicles)
    delivery_fee = (
        DELIVERY_FEE
        if ordered_vehicles and subtotal < DELIVERY_THRESHOLD
        else Decimal("0.00")
    )

    return {
        "selected_vehicle_ids": parsed_ids,
        "selected_vehicles": ordered_vehicles,
        "selected_vehicle_count": len(ordered_vehicles),
        "selected_vehicle_subtotal": subtotal,
        "selected_vehicle_subtotal_display": f"{subtotal:,}",
        "selected_vehicle_delivery_fee": delivery_fee,
        "selected_vehicle_total": Decimal(subtotal) + delivery_fee,
    }
